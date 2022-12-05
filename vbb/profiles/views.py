import re
from datetime import datetime

import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, send_mail
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from rest_framework import permissions, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from vbb.libraries.models import Library
from vbb.organizations.models import Organization
from vbb.profiles.models import MentorProfile, StudentProfile, Opportunity
from vbb.profiles.serializers import OpportunitySerializer
from vbb.users.admin import User
from vbb.users.api.serializers import UserSerializer
from vbb.users.models import TIMEZONES
from vbb.utils.custom_csrf import CsrfHTTPOnlySessionAuthentication
from rest_framework import viewsets


class OpportunityViewSet(viewsets.ModelViewSet):
    """
    Genre Views from Rest Framework
    """

    authentication_classes = ()
    permission_classes = []
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer



class MentorSignUp(APIView):
    """Public Mentor Sign Up view"""

    authentication_classes = ()
    permission_classes = []

    def post(self, request: Request) -> Response:
        """
        Manages Mentor Sign Up

        data example:{
            "email": "will@test.com",
            "name": "Test Mentor Signup",
            "password": ""
            }
        """
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        password = request.data.get("password")
        confirmPW = request.data.get("confirm_password")
        corporate_code = request.data.get("corporate_code", "")

        name = first_name + ' ' + last_name

        assigned_library = None
        org = None


        if len(email) > 45:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Email must be less than 45 characters, and must be unique."},
            )


        try:
            # validate the username
            existingEmail = User.objects.get(email=email)

            if existingEmail:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"error": "A user with that email already exists."},
                )
        except ObjectDoesNotExist:
            pass

        if password != confirmPW:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Passwords must match."},
            )

        # Look up Organization by corp code
        if corporate_code != "" and corporate_code != None:
            try:
                org = Organization.objects.get(corporate_code=corporate_code)
                assigned_library = org.library
            except Organization.DoesNotExist:

                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": "A corporate/charter organization with that code does not exist. Please try again with a valid code."},
                )

        try:
            user = User.objects.create(first_name=first_name, last_name=last_name,name=name,  is_mentor=True, email=email, is_active=False)
            user.set_password(password)
            user.save()

            if assigned_library:
                mentorProfile = MentorProfile.objects.create(assigned_library=assigned_library, organization=org, user=user, is_onboarded=False)
                mentorProfile.save()
            else:
                mentorProfile = MentorProfile.objects.create(user=user, is_onboarded=False)
                mentorProfile.save()


            link = settings.EMAIL_LINK
            # Still needs to send email
            if user:
                token = jwt.encode(
                    {"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256"
                )
                link = link + f"?token={token}"
                print(f"email link: {link}")
            # amazon simple email service
            # send_mail("subject", "message", "from_email", ["to_list"])

            msg = EmailMessage(
              from_email='mentor@villagebookbuilders.org',
              to=[user.email],
            )

            msg.template_id = "d-e5a5f3e91ebe4621a24355673ae255f2"
            msg.dynamic_template_data = {
              "first_name": user.first_name,
              "verification_link": link
            }
            msg.subject = "Welcome to Village Book Builders! Please verify your account to finish setup."
            print(msg.dynamic_template_data)

            try:
                msg.send(fail_silently=False)
            except Exception as e:
                print(e)


            # body = f"Welcome to Village Book Builders! Please confirm your email by copy and pasting this link in your browser: {link}"
            # send_mail(
            #     "Village Book Builders - Please confirm your email",
            #     body,
            #     "mentor@villagebookbuilders.org",
            #     [user.email],
            # )
            return Response(status=status.HTTP_201_CREATED, data={"message": "Email verification link sent successfully"})

        except IntegrityError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Email is already taken"},
            )


class MentorConfirmationEmailViewSet(APIView):
    authentication_classes = ()
    permission_classes = []

    def post(self, request: Request) -> Response:
        """
        Updates user.is_email_verified to true if JWT can be decoded

        Returns:
            Redirect to base_url + 'login/' on success
            HTTP_403_FORBIDDEN,
            HTTP_500_INTERNAL_SERVER_ERROR if the root uri
        """
        token = request.data.get("token")

        if not token:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            decoded_token = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message":"Could not decode JWT."})

        try:
            user = User.objects.get(id=decoded_token.get("user_id"))
            user.is_email_verified = True
            user.is_active = True
            user.role = 2
            user.save()

            return Response(
                status=status.HTTP_200_OK,
                data={"message": "Successfully verified your email!"},
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)


class MentorProfileViewSet(APIView):
    """
    Mentor Profile Views from Rest Framework
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Register Mentor form
        example data = {
            "careers": [14],
            "mentoring_languages": [14, 8],
            "subjects": [2, 8],
            "application_video_url": "",
            "interests": "life laughter",
            "phone_number": "202-1234569",
            "secondary_email": "secondEmail@test.co",
            "corporate_code": "corp code",
            "is_of_age": True,
            "timezone": "Indian/Christmas",
            "date_of_birth": "mm/dd/yyyy"
        }
        """
        user = request.user
        data = request.data
        career_ids = data.get("careers", [])
        mentoring_language_ids = data.get("mentoring_languages", [])
        opportunities = data.get("opportunities", [])
        subject_ids = data.get("subjects", [])
        application_video_url = data.get("application_video_url", "")
        interests = data.get("interests", "")
        phone_number = data.get("phone_number", "")
        secondary_email = data.get("secondary_email", "")
        #corporate_code = data.get("corporate_code", "")
        is_of_age = data.get("is_of_age", False)
        time_zone = data.get("timezone", "")
        date_of_birth = data.get("date_of_birth")
        crimesOrMisdemeanor = data.get("crimes_or_misdemeanor", False)
        crimesOrMisdemeanorResponses = data.get("crimes_or_misdemeanor_responses", "")
        gender = data.get("gender", "")

        # Look up Organization by corp code
        # try:
        #     org = Organization.objects.get(corporate_code=corporate_code)
        #     assigned_library = org.library
        # except Organization.DoesNotExist:
        #     assigned_library = None
        #     org = None

        print(data)


        time_zones = dict(TIMEZONES)
        user_time_zone = time_zones.get(time_zone)
        if user_time_zone:
            user.time_zone = user_time_zone

        if date_of_birth:
            user.date_of_birth = datetime.strptime(date_of_birth, "%m/%d/%Y")

        if gender:
            user.gender = gender

        # user.is_mentor = True
        user.save()
        user.refresh_from_db()

        (mentor_profile, _) = MentorProfile.objects.update_or_create(
            # criteria for the get value
            user=user,
            defaults={
                # values used to update or create
                "application_video_url": application_video_url,
                # approval_status : models.CharField(
                #     max_length:30,
                #     choices:MentorApprovalStatus.choices,
                #     default:MentorApprovalStatus.NOT_REVIEWED,
                # )
                # has_viewed_donation_page : models.BooleanField(default=False)
                # has_completed_training : models.BooleanField(default=False)
                # has_clicked_facebook_workplace_invite : models.BooleanField(default=False)
                "crimesOrMisdemeanor":crimesOrMisdemeanor,
                "crimesOrMisdemeanorResponses":crimesOrMisdemeanorResponses,
                "interests": interests,
                "phone_number": phone_number,
                "secondary_email": secondary_email,
                "is_of_age": is_of_age,
            },
        )

        print(opportunities)
        mentor_profile.opportunities.set(opportunities)
        mentor_profile.careers.set(career_ids)
        mentor_profile.mentoring_languages.set(mentoring_language_ids)
        mentor_profile.subjects.set(subject_ids)
        mentor_profile.is_onboarded = True
        mentor_profile.save()

        serialized_user = UserSerializer(
            user,
            context={"request": request},
        )
        return Response(status=status.HTTP_201_CREATED, data=serialized_user.data)


class ApproveStudentViewSet(APIView):
    """
    Mentor Profile Views from Rest Framework
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Approve Student form
        example data = {

        }
        """
        user = request.user

        library = {}
        studentProfile = None

        student_id = request.data.get("student_id", None)
        stat = request.data.get("status", None)


        try:
            student = User.objects.get(pk=student_id)
        except User.DoesNotExist:
            return Response({"error": "User with that provided ID could not be found."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            studentProfile = StudentProfile.objects.get(user=student_id)
        except StudentProfile.DoesNotExist:
            return Response({"error": "StudentProfile with that provided ID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        if stat == "approved":
            studentProfile.approval_status = 'Approved'
        elif stat == "not-reviewed":
            studentProfile.approval_status = 'Not Reviewed'
        elif stat == "rejected":
            studentProfile.approval_status = 'Rejected'
        else:
            return Response({"error": "Status provided not a valid status."}, status=status.HTTP_400_BAD_REQUEST)


        studentProfile.save()

        serialized_user = UserSerializer(
            user,
            context={"request": request},
        )
        return Response({"user": serialized_user.data},status=status.HTTP_201_CREATED)

class ApproveMentorViewSet(APIView):
    """
    Mentor Profile Views from Rest Framework
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Approve Mentor form
        example data = {

        }
        """
        user = request.user

        library = {}
        mentorProfile = None

        mentor_id = request.data.get("mentor_id", None)
        library_id = request.data.get("library_id", None)
        stat = request.data.get("status", None)


        try:
            mentor = User.objects.get(pk=mentor_id)
        except User.DoesNotExist:
            return Response({"error": "User with that provided ID could not be found."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            library = Library.objects.get(uniqueID=library_id)
        except Library.DoesNotExist:
            return Response({"error": "Library with that provided ID could not be found."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            mentorProfile = MentorProfile.objects.get(user=mentor)
        except MentorProfile.DoesNotExist:
            return Response({"error": "StudentProfile with that provided ID could not be found."}, status=status.HTTP_400_BAD_REQUEST)

        if stat == "approved":
            mentorProfile.approval_status = 'Approved'
            mentorProfile.assigned_library = library

        elif stat == "not-reviewed":
            mentorProfile.approval_status = 'Not Reviewed'
        elif stat == "rejected":
            mentorProfile.approval_status = 'Rejected'
        else:
            return Response({"error": "Status provided not a valid status."}, status=status.HTTP_400_BAD_REQUEST)


        mentorProfile.save()

        serialized_user = UserSerializer(
            user,
            context={"request": request},
        )
        return Response({"user": serialized_user.data},status=status.HTTP_201_CREATED)


class StudentSignUp(APIView):
    """Public Student Sign Up view"""

    authentication_classes = ()
    permission_classes = []

    def post(self, request: Request) -> Response:
        """
        Manages Student Sign Up

        data example:{
            "email": "will@test.com",
            "name": "Test Mentor Signup",
            "password": ""
            }
        """
        username = request.data.get("username")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        password = request.data.get("password")
        confirmPW = request.data.get("confirm_password")
        library_code = request.data.get("library_code")

        name = first_name + ' ' + last_name


        if len(username) > 45:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Username must be less than 45 characters, and must be unique."},
            )


        try:
            # validate the username
            existingUsername = User.objects.get(username=username)

            if existingUsername:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": "A user with that username already exists."},
                )

        except ObjectDoesNotExist:
            pass

        if password != confirmPW:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Passwords must match."},
            )

        # validate the library code
        try:
            assigned_library = Library.objects.get(library_code=library_code)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "A Library could not be found with the code provided."},
            )


        try:
            user = User.objects.create(first_name=first_name, last_name=last_name,name=name,  is_student=True, username=username, role=1)
            user.set_password(password)
            user.save()

            userProfile = StudentProfile.objects.create(assigned_library=assigned_library, user=user, is_onboarded=False)
            userProfile.save()

            return Response(status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Email is already taken"},
            )


class StudentProfileViewSet(APIView):
    """
    Student Profile Views from Rest Framework


    Students register fro the root page and create a user at the same time,
    so there is no user logged in
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Register Student form
        example data = {
            "careers_of_interest": [10, 1, 8],
            "interests": "Other stuff I'm interested in",
            "library_code": "bad_code",
            "mentoring_languages": [],
            "name": "Test Student",
            "password": "123",
            "subjects": [5, 7, 3],
            "timezone": "Africa/Bujumbura",
            "username": "test_student1",
        }
        """
        user = request.user
        data = request.data
        print(data)
        careers_of_interest = data.get("careers", [])
        mentoring_language_ids = data.get("mentoring_language_ids", [])
        favorite_genres_ids = data.get("favorite_genres_ids", [])
        subject_ids = data.get("subject_ids", [])
        struggle_subject_ids = data.get("struggle_subject_ids", [])
        library_code = data.get("library_code", "")
        time_zone = data.get("timezone", "")
        family_status = data.get("family_status", "")
        family_support_level = data.get("family_support_level", "")
        graduation_obstacle = data.get("graduation_obstacle", "")
        grade_level = data.get("grade_level", "")
        year_of_birth = data.get("year_of_birth", "")
        gender = data.get("gender", "")

        # validate the library code
        # try:
        #     print(data)
        #     assigned_library = Library.objects.get(library_code=library_code)
        # except ObjectDoesNotExist:
        #     return Response(
        #         status=status.HTTP_400_BAD_REQUEST,
        #         data={"message": "Library with the code provided was not found."},
        #     )

        # create user
        time_zones = dict(TIMEZONES)
        user_time_zone = time_zones.get(time_zone)

        if year_of_birth:
            user.date_of_birth = year_of_birth


        if user_time_zone:
            user.time_zone = user_time_zone

        if gender:
            user.gender = gender

        user.save()
        user.refresh_from_db()

        try:
            (student_profile, _) = StudentProfile.objects.update_or_create(
                # criteria for the get value
                user=user,
                defaults={
                    # values used to update or create
                    "family_status": family_status,
                    "family_support_level": family_support_level,
                    "graduation_obstacle": graduation_obstacle,
                    "grade_level": grade_level,
                },
            )

            student_profile.careers_of_interest.add(*careers_of_interest)
            student_profile.mentoring_languages.add(*mentoring_language_ids)
            student_profile.subjects.add(*subject_ids)
            student_profile.favorite_genres.add(*favorite_genres_ids)
            student_profile.is_onboarded = True
            student_profile.save()

        except IntegrityError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Student profile is already created."},
            )

        serialized_user = UserSerializer(
            user,
            context={"request": request},
        )
        return Response(status=status.HTTP_201_CREATED, data=serialized_user.data)
