import os
from oauth2client import file, client
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from googleapiclient import _auth
from apiclient import errors
import base64
import requests
import requests_oauth2
from requests_oauth2 import OAuth2BearerToken

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from bs4 import BeautifulSoup
import re
import random
import string
import environ
import json
import base64
from pathlib import Path
import configparser
from vbb.meetings.graph import Graph

# from dateutil.relativedelta import relativedelta
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


class google_apis:
  ''''
  FUNCTIONS:
  1) account_create(self, firstName, lastName, personalEmail)
    - creates a mentor account
  2) calendar_event(self, menteeEmail, mentorEmail, personalEmail, directorEmail, start_time, end_date, calendar_id, room, duration=.5)
    - creates a calendar event with a google meets link
  3) email_send(self, to, subject, templatePath, extraData=None, cc=None)
    - sends welcome email
  '''
  __webdev_cred = ''
  __mentor_cred = ''

  def __init__(self):
    env = environ.Env()

    # the proper scopes are needed to access specific Google APIs
    # see https://developers.google.com/identity/protocols/oauth2/scopes
    scopes = [
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/gmail.compose',
      'https://www.googleapis.com/auth/admin.directory.user',
      'https://www.googleapis.com/auth/admin.directory.group',
    ]

    dirname = os.path.dirname(__file__)

    env.read_env(str(ROOT_DIR / ".env"))

    serviceKey = env("GOOGLE_SERVICE_KEY", default="")

    print('Key:')
    #print(serviceKey)

    decoded = base64.b64decode(serviceKey).decode('utf-8')
    #print(decoded)

    fileObj = json.loads(decoded)
    print(fileObj)

    #print(file)
    SERVICE_ACCOUNT_FILE = os.path.join(dirname, "service-account.json")
    credentials = service_account.Credentials.from_service_account_info(
            fileObj, scopes=scopes)
    self.__webdev_cred = credentials.with_subject(
        'webdevelopment@villagebookbuilders.org')
    self.__mentor_cred = credentials.with_subject(
        'mentor@villagebookbuilders.org')

  def account_create(self, firstName, lastName, personalEmail):
    http = _auth.authorized_http(self.__webdev_cred)
    self.__webdev_cred.refresh(http._request)
    url = "https://www.googleapis.com/admin/directory/v1/users"
    headers = {
      # 'Authorization': 'Bearer' delegated_credentials.token,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
    # checking if the email id already exists, adds an id to the end to differentiate
    addedID = 0  # on repeat, email will start from firstname.lastname1@villagementors.org

    def userExists(email):
      url = 'https://www.googleapis.com/admin/directory/v1/users/' + email
      with requests.Session() as s:
        s.auth = OAuth2BearerToken(self.__webdev_cred.token)
        r = s.get(url)
        if (r.status_code == 404):
          return False
        return True

    primaryEmail = firstName + '.' + lastName + '@villagementors.org'

    while(userExists(primaryEmail)):
      addedID += 1
      primaryEmail = firstName + '.' + lastName + \
          str(addedID) + '@villagementors.org'
    pwd = 'VBB' + random.choice(['!', '@', '#', '$', '%', '&']) + \
                                str(random.randint(100000000, 1000000000))

    data = '''
    {
      "primaryEmail": "%s",
      "name": {
        "familyName": "%s",
        "givenName": "%s"
      },
      "password": "%s",
      "changePasswordAtNextLogin": "true",
      "recoveryEmail": "%s",
    }
    ''' % (primaryEmail, lastName, firstName, pwd, personalEmail)

    with requests.Session() as s:
      s.auth = OAuth2BearerToken(self.__webdev_cred.token)
      r = s.post(url, headers=headers, data=data)
    return (primaryEmail, pwd)

  def calendar_event(self, mentorFirstName, mentorEmail, directorEmail, start_time, end_date, calendar_id, room, duration, isRecurring, recurringEndDate=None):
    calendar_service = build('calendar', 'v3', credentials=self.__mentor_cred)
    timezone = 'UTC'
    start_date_time_obj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
    end_time = start_date_time_obj + timedelta(hours=1)
    end_date_formated = end_date.replace(':', '')
    end_date_formated = end_date_formated.replace('-', '')
    end_date_formated += 'Z'

    if recurringEndDate and isRecurring == True:
        print(recurringEndDate)
        recurringEndDate = recurringEndDate.strip('Z')
        endrecurr_obj = datetime.strptime(recurringEndDate, '%Y-%m-%dT%H:%M:%S')
        endrecurr_obj_formated = recurringEndDate.replace(':', '')
        endrecurr_obj_formated = endrecurr_obj_formated.replace('-', '')
        endrecurr_obj_formated += 'Z'
        print(endrecurr_obj_formated)


    event = {}


    if isRecurring == True:
        recurrenceString = 'RRULE:FREQ=WEEKLY;UNTIL='+ endrecurr_obj_formated
        print(recurrenceString)

        event = {
          'summary': mentorFirstName + ' - VBB Mentoring Session',
          'start': {
            'dateTime': start_date_time_obj.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
          },
          'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
          },
          'recurrence': [
            recurrenceString
          ],
          'attendees': [
            {'email': mentorEmail},
            {'email': directorEmail},
            {'email': room, 'resource': "true"}
          ],
          'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},  # reminder 24 hrs before event
            # pop up reminder, 10 min before event
            {'method': 'popup', 'minutes': 10},
            ],
          },
          'conferenceData': {
            'createRequest': {
              'requestId': ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            }
          },
        }

    else:
        event = {
          'summary': mentorFirstName + ' - VBB Mentoring Session',
          'start': {
            'dateTime': start_date_time_obj.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
          },
          'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
          },
          'attendees': [
            {'email': mentorEmail},
            {'email': directorEmail},
            {'email': room, 'resource': "true"}
          ],
          'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},  # reminder 24 hrs before event
            # pop up reminder, 10 min before event
            {'method': 'popup', 'minutes': 10},
            ],
          },
          'conferenceData': {
            'createRequest': {
              'requestId': ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            }
          },
        }

    print(event)

    event_obj = calendar_service.events().insert(calendarId=calendar_id, body=event,
                                        sendUpdates="all", conferenceDataVersion=1).execute()

    print(event_obj)

    print ("hangoutlink", event_obj['hangoutLink'])

    payload = {"id":event_obj['id'], "link": event_obj['hangoutLink']}
    return(payload)

  def email_send(self, to, subject, templatePath, extraData=None, cc=None):
    """
    to: recipient
    cc: python array, carbon copy recipients
    """
    http = _auth.authorized_http(self.__mentor_cred)
    email_service = build('gmail', 'v1', http=http)
    personalizedPath = os.path.join(
        "api", "emails", "templates", "placeholder.html")
    if cc is not None:
      cc = ','.join(cc)

    def updatePersonalizedHTML(templatePath, personalizedPath, extraData):
      """ Get HTML with the extraData filled in where specified.
      - Use Beautiful soup to find and replace the placeholder values with the proper user
        specific info
      - use 'with' to write the beautifulSoup string into a newFile - the personalized version of the
        original templatePath. This personalized version will be sent out in the email and will be
        rewritten everytime the function is called.
      """
      with open(templatePath, 'r', encoding="utf8") as f:
        template = f.read()
      # soup = BeautifulSoup(template, features="html.parser")
      # if extraData != None:
      #   for key in extraData:
      #     target = soup.find_all(text=re.compile(r'%s' % key))
      #     for v in target:
      #       v.replace_with(v.replace('%s' % key, extraData[key]))
      #   # now soup string has the proper values
      # with open(personalizedPath, "w") as file:
      #   file.write(str(soup))

    def create_message(to, subject, personalizedPath, cc=None):
      """Create a message for an email.

      Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        personalizedPath: File path to email in html file with variable replaced
                  with proper values.

      Returns:
        An object containing a base64url encoded email object.
      """
      f = open(personalizedPath, 'r')
      message_text = f.read()
      sender = self.__mentor_cred._subject
      message = MIMEText(message_text, 'html')
      message['to'] = to
      message['cc'] = cc
      message['from'] = sender
      message['subject'] = subject
      # the message should converted from string to bytes.
      message_as_bytes = message.as_bytes()
      # encode in base64 (printable letters coding)
      message_as_base64 = base64.urlsafe_b64encode(message_as_bytes)
      raw = message_as_base64.decode()  # need to JSON serializable
      return {'raw': raw}

    def send_message(service, user_id, message):
      """Send an email message.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

      Returns:
        Sent Message.
      """
      try:
        message = (email_service.users().messages().send(userId=user_id, body=message)
                  .execute())
        # print('Message Id: %s' % message['id'])
        return message
      except errors.HttpError as error:
        print('An error occurred: %s' % error)
    # updatePersonalizedHTML(templatePath, personalizedPath, extraData)
    msg = create_message(to, subject, personalizedPath, cc)
    send_message(email_service, "me", msg)

  def group_subscribe(self, groupEmail, userEmail):
    http = _auth.authorized_http(self.__webdev_cred)
    self.__webdev_cred.refresh(http._request)
    url = "https://www.googleapis.com/admin/directory/v1/groups/" + groupEmail + "/members"
    headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
    data = '''
    {
      "email": "%s",
      "role": "MEMBER",
    }
    ''' % (userEmail)
    with requests.Session() as s:
      s.auth = OAuth2BearerToken(self.__webdev_cred.token)
      r = s.post(url, headers=headers, data=data)
      # print(r.text)

  def classroom_invite(self, courseID, email, role="TEACHER"):
    cred = self.__mentor_cred
    http = _auth.authorized_http(cred)
    cred.refresh(http._request)
    url = "https://classroom.googleapis.com/v1/invitations"
    headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
    data = '''
    {
      "userId": "%s",
      "courseId": "%s",
      "role": "%s",
    }
    ''' % (email, courseID, role)
    with requests.Session() as s:
      s.auth = OAuth2BearerToken(cred.token)
      r = s.post(url, headers=headers, data=data)

  def course_list(self, teacherEmail):
    cred = self.__mentor_cred
    http = _auth.authorized_http(cred)
    cred.refresh(http._request)
    url = "https://classroom.googleapis.com/v1/courses?courseStates=ACTIVE&teacherId="+teacherEmail
    headers = {
      'Accept': 'application/json',
    }
    with requests.Session() as s:
      s.auth = OAuth2BearerToken(cred.token)
      r = s.get(url, headers=headers)
      return r.text

  def update_event(self, calendar_id, event_id, end_date=None, start_time=None, end_time=None):
    calendar_service = build('calendar', 'v3', credentials=self.__mentor_cred)
    event = calendar_service.events().get(
        calendarId=calendar_id, eventId=event_id).execute()
    if (end_date != None):
      end_date_formated = end_date.replace(':', '')
      end_date_formated = end_date_formated.replace('-', '')
      end_date_formated += 'Z'
      event['recurrence'] = ['RRULE:FREQ=WEEKLY;UNTIL=' + end_date_formated]

   # event['summary'] = 'update worked'
    updated_event = calendar_service.events().update(
        calendarId=calendar_id, eventId=event['id'], body=event).execute()


    # return updated_event['recurrence'] = []

  def shift_event(self, calendar_id, event_id):
    calendar_service = build('calendar', 'v3', credentials=self.__mentor_cred)
    event = calendar_service.events().get(
        calendarId=calendar_id, eventId=event_id).execute()
    # print('event_id: ' , event_id)
    event['start']['timeZone'] = "UTC"
    event['end']['timeZone'] = "UTC"
   # event['summary'] = 'update worked'
    updated_event = calendar_service.events().update(
        calendarId=calendar_id, eventId=event['id'], body=event).execute()
    # print('updated_event: ', updated_event)
    #return updated_event['recurrence'] = []

  def remove_end_date(self, calendar_id, event_id):
    calendar_service = build('calendar', 'v3', credentials=self.__mentor_cred)
    event = calendar_service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    # print('event_id: ' , event_id)
    event['recurrence'] = ['RRULE:FREQ=WEEKLY']
    updated_event = calendar_service.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()
    # print('updated_event: ', updated_event)
    #return updated_event['recurrence'] = []


class ms_apis:
  def __init__(self):
    env = environ.Env()
    # the proper scopes are needed to access specific Google APIs
    # see https://developers.google.com/identity/protocols/oauth2/scopes
    config = configparser.ConfigParser()

    #configPath = os.path.join(os.getcwd(),'ms_config.cfg')

    path = os.path.dirname(os.path.realpath(__file__))
    configPath = os.path.join(path,'ms_config.cfg')

    config.read(configPath)
    # print(configPath)
    # print(config)
    # print(config.sections())
    self.azure_settings = config['azure']

    self.graph: Graph = Graph(self.azure_settings)
    env.read_env(str(ROOT_DIR / ".env"))

    #serviceKey = env("GOOGLE_SERVICE_KEY", default="")
  def generateMSCalendarEvent(graph: Graph, studentName, mentorName, mentorEmail, directorEmail, start_time, end_time, isRecurring, recurringEndDate):
    # Note: if using app_client, be sure to call
    # ensure_graph_for_app_only_auth before using it
    #print(self)
    print(graph.graph)
    graph.graph.ensure_graph_for_app_only_auth()

    users = graph.graph.get_users()
    print(users)
    createdEvent = graph.graph.createEvent(studentName, mentorName, mentorEmail, directorEmail, start_time, end_time, isRecurring, recurringEndDate)
    # TODO
    print(createdEvent)
    return createdEvent

  def display_access_token(graph: Graph):
    token = graph.get_user_token()
    print('User token:', token, '\n')

  def list_calendar_events(graph: Graph):
    # TODO
    return

  def list_users(graph: Graph):
    users_page = graph.get_users()

    # Output each users's details
    for user in users_page['value']:
        print('User:', user['displayName'])
        print('  ID:', user['id'])
        print('  Email:', user['mail'])

    # If @odata.nextLink is present
    more_available = '@odata.nextLink' in users_page
    print('\nMore users available?', more_available, '\n')

def generateCalendarEvent(studentName, mentorEmail, directorEmail, dateStart, dateEnd, location, isRecurring, recurringEndDate, conferenceType="google"):
    eventObj = {}
    print(recurringEndDate)
    if conferenceType == "google":
        g = google_apis()
        eventObj = g.calendar_event(
                studentName,
                mentorEmail,
                directorEmail,
                dateStart, dateEnd,
                "c_nqd1aak2qnc6j4ejejo787qk1o@group.calendar.google.com",
                location,
                "c_188apa1pg08nkg9pn621lmhbfc0f04gnepkmor31ctim4rrfddh7aqbcchin4spedtp6e@resource.calendar.google.com", isRecurring, recurringEndDate)
    elif conferenceType == "ms-teams":
         m = ms_apis()
         msEvent = m.generateMSCalendarEvent(
                studentName,
               "Mentor",
               mentorEmail,
               directorEmail,
               dateStart,
               dateEnd,
               isRecurring,
               recurringEndDate)

         eventObj = {"link":msEvent["onlineMeeting"]["joinUrl"],"id":msEvent["id"]}
    else:
        eventObj = None

    return eventObj

  # FOR TESTING PURPOSES -- REMOVE LATER
# def testFunction():
#   m = ms_apis()
#   m.generateMSCalendarEvent(
#         "Test Student",
#         "Mentor One",
#         "chris@myrelaytech.com",
#         "director@villagebookbuilders.org",
#         "2022-12-23T13:30:00",
#         "2022-12-23T14:00:00",
#         False,
#         "2022-12-23T14:00:00")

  # g.calendar_event(
  #       "Mentor One",
  #       "chris@myrelaytech.com",
  #       "chris@myrelaytech.com",
  #       "2020-12-23T13:30:00",
  #       "2020-12-23T14:00:00",
  #       "-",
  #      "ximena.rodriguez1@villagementors.org",
  #     "c_188apa1pg08nkg9pn621lmhbfc0f04gnepkmor31ctim4rrfddh7aqbcchin4spedtp6e@resource.calendar.google.com")

  #g = google_apis()
  #g.shift_event("c_oha2uv7abp2vs6jlrl96aeoje8@group.calendar.google.com","0vjr0aj0e3nv1tmc2ui2mtshbi")


  #g = google_apis()
  #print("subscribing")
  #g = google_apis()
  #print("subscribing")
  #g.group_subscribe("mentor.collaboration@villagebookbuilders.org", "ed.ringger@villagementors.org")
  # welcome_mail = os.path.join("api", "emails", "templates", "welcomeLetter.html")
  #
  # sessionConfirm_mail = os.path.join("api","emails","templates", "sessionConfirm.html")
  # training_mail = os.path.join("api","emails","templates", "training.html")
  # newMentorNotice_mail = os.path.join("api","emails","templates", "newMentorNotice.html")
#
#   g.email_send(
#    "edringger@gmail.com",        # personal email form form
#    "Welcome to the VBB Family!",
#    welcome_mail,
#    {
#      '__first_name': "Shwetha",                 # first name from form
#      '__new_email': "varunvraja@gmail.com",         # email generated by shweta's code
#      '__password': "vbb"                        # password generated by shweta's code
#    },
#    ["ed.test1@villagebookbuilders.org", "ed.ringger0@villagementors.org"]
#   )
#
#   g.email_send(
#     "ed.test1@villagebookbuilders.org",        # personal email form form
#     "Training",
#     training_mail,
#     cc=["edringger@gmail.com"]
#   )
#
# g.calendar_event(
#       "Mentor One",
#       "chris@myrelaytech.com",
#       "chris@myrelaytech.com",
#       "2020-12-23T13:30:00",
#       "2020-12-23T14:00:00",
#       "-",
#      "ximena.rodriguez1@villagementors.org",
#     "c_188apa1pg08nkg9pn621lmhbfc0f04gnepkmor31ctim4rrfddh7aqbcchin4spedtp6e@resource.calendar.google.com")

#  g.update_event(
#
# #      "sohatesttß@villagementors.org",
#    "ximena.rodriguez1@villagementors.org",
#       "shwetha@gmail.com",
#       "shwetha@gmail.com",
#      "2020-10-23T23:30:00", "2020-12-10T22:00:00",
#  # "c_oha2uv7abp2vs6jlrl96aeoje8@group.calendar.google.com",
#   "ximena.rodriguez1@villagementors.org",
#  # "ljg8ar4q4e5l2hg18h4epqtc34",
#  # "2022-10-27T22:00:00")
#    "c_188apa1pg08nkg9pn621lmhbfc0f04gnepkmor31ctim4rrfddh7aqbcchin4spedtp6e@resource.calendar.google.com")
#
#   print("updated")

#testFunction()
