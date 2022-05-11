import re
from datetime import datetime

import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from rest_framework import permissions, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from vbb.libraries.models import Library
from vbb.organizations.models import Organization
from vbb.profiles.models import MentorProfile, StudentProfile
from vbb.users.admin import User
from vbb.users.api.serializers import UserSerializer
from vbb.users.models import TIMEZONES
from vbb.utils.custom_csrf import CsrfHTTPOnlySessionAuthentication


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
        name = request.data.get("name")
        password = request.data.get("password")

        try:
            user = User.objects.create(name=name, email=email)
            user.set_password(password)
            user.save()

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
            body = f"Welcome to Village Book Builders! Please confirm your email by clicking this link: {link}"
            send_mail(
                "Village Book Builders - Please confirm your email",
                body,
                "test@test.com",
                [user.email],
            )
            return Response(status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Email is already taken"},
            )


class MentorConfirmationEmailViewSet(APIView):
    authentication_classes = ()
    permission_classes = []

    def get(self, request: Request):
        """
        Updates user.is_email_verified to true if JWT can be decoded

        Returns:
            Redirect to base_url + 'login/' on success
            HTTP_403_FORBIDDEN,
            HTTP_500_INTERNAL_SERVER_ERROR if the root uri
        """
        token = request.query_params.get("token")
        if not token:
            return Response(status=status.HTTP_403_FORBIDDEN)

        decoded_token = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.get(id=decoded_token.get("user_id"))
            user.is_email_verified = True
            user.save()

            full_url = request.build_absolute_uri()
            try:
                # regex
                # 'http://vbb.local/api/v1/mentor-sign-up/' -> ['http://vbb.local/']
                base_url = re.findall("^.*?(?=api)", full_url)[0]
                redirect_url = base_url + "login"
                return HttpResponseRedirect(redirect_to=redirect_url)
            except IndexError:
                # regex failed to pull the root uri
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    data={"message": "Error parsing root uri"},
                )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)


class MentorProfileViewSet(APIView):
    """
    Mentor Profile Views from Rest Framework
    """

    authentication_classes = (CsrfHTTPOnlySessionAuthentication, BasicAuthentication)
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
        data = request.data.get("data", {})
        career_ids = data.get("careers", [])
        mentoring_language_ids = data.get("mentoring_languages", [])
        subject_ids = data.get("subjects", [])
        application_video_url = data.get("application_video_url", "")
        interests = data.get("interests", "")
        phone_number = data.get("phone_number", "")
        secondary_email = data.get("secondary_email", "")
        corporate_code = data.get("corporate_code", "")
        is_of_age = data.get("is_of_age", False)
        time_zone = data.get("timezone", "")
        date_of_birth = data.get("date_of_birth")
        # Look up Organization by corp code
        try:
            org = Organization.objects.get(corporate_code=corporate_code)
            assigned_library = org.library
        except Organization.DoesNotExist:
            assigned_library = None
            org = None

        time_zones = dict(TIMEZONES)
        user_time_zone = time_zones.get(time_zone)
        if user_time_zone:
            user.time_zone = user_time_zone

        if date_of_birth:
            user.date_of_birth = datetime.strptime(date_of_birth, "%m/%d/%Y")

        user.is_mentor = True
        user.save()
        user.refresh_from_db()
        (mentor_profile, _) = MentorProfile.objects.update_or_create(
            # criteria for the get value
            user=user,
            defaults={
                # values used to update or create
                "assigned_library": assigned_library,
                "organization": org,
                "application_video_url": application_video_url,
                # approval_status : models.CharField(
                #     max_length:30,
                #     choices:MentorApprovalStatus.choices,
                #     default:MentorApprovalStatus.NOT_REVIEWED,
                # )
                # has_viewed_donation_page : models.BooleanField(default=False)
                # has_completed_training : models.BooleanField(default=False)
                # has_clicked_facebook_workplace_invite : models.BooleanField(default=False)
                "interests": interests,
                "phone_number": phone_number,
                "secondary_email": secondary_email,
                "is_of_age": is_of_age,
            },
        )

        mentor_profile.careers.add(*career_ids)
        mentor_profile.mentoring_languages.add(*mentoring_language_ids)
        mentor_profile.subjects.add(*subject_ids)
        mentor_profile.save()

        serialized_user = UserSerializer(
            user,
            context={"request": request},
        )
        return Response(status=status.HTTP_201_CREATED, data=serialized_user.data)


class StudentProfileViewSet(APIView):
    """
    Student Profile Views from Rest Framework


    Students register fro the root page and create a user at the same time,
    so there is no user logged in
    """

    authentication_classes = ()
    permission_classes = []

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

        data = request.data.get("data", {})
        careers_of_interest = data.get("careers_of_interest", [])
        mentoring_language_ids = data.get("mentoring_languages", [])
        subject_ids = data.get("subjects", [])
        library_code = data.get("library_code", "")

        username = data.get("username")
        password = data.get("password")
        name = data.get("name")
        time_zone = data.get("timezone", "")

        # validate the library code
        try:
            assigned_library = Library.objects.get(library_code=library_code)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Library code provided was not found."},
            )

        # create user
        time_zones = dict(TIMEZONES)
        user_time_zone = time_zones.get(time_zone)
        try:
            user = User.objects.create(
                username=username, name=name, time_zone=user_time_zone
            )
        except IntegrityError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Username is already taken."},
            )

        # this hashes the password
        user.set_password(password)
        user.is_student = True
        user.save()
        user.refresh_from_db()

        is_verified = True if assigned_library else False
        (student_profile, _) = StudentProfile.objects.update_or_create(
            # criteria for the get value
            user=user,
            defaults={
                # values used to update or create
                "assigned_library": assigned_library,
                "is_verified": is_verified,
            },
        )

        student_profile.careers_of_interest.add(*careers_of_interest)
        student_profile.mentoring_languages.add(*mentoring_language_ids)
        student_profile.subjects.add(*subject_ids)
        student_profile.save()

        serialized_user = UserSerializer(
            user,
            context={"request": request},
        )
        return Response(status=status.HTTP_201_CREATED, data=serialized_user.data)
