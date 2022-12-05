import json
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from msgraph.core import GraphClient
import datetime

class Graph:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client: GraphClient
    client_credential: ClientSecretCredential
    app_client: GraphClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['authTenant']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        self.user_client = GraphClient(credential=self.device_code_credential, scopes=graph_scopes)

    def ensure_graph_for_app_only_auth(self):
        if not hasattr(self, 'client_credential'):
            client_id = self.settings['clientId']
            tenant_id = self.settings['tenantId']
            client_secret = self.settings['clientSecret']

            self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)

        if not hasattr(self, 'app_client'):
            self.app_client = GraphClient(credential=self.client_credential,
                                          scopes=['https://graph.microsoft.com/.default'])

    def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.device_code_credential.get_token(graph_scopes)
        return access_token.token

    def get_users(self):
        self.ensure_graph_for_app_only_auth()

        endpoint = '/users'
        # Only request specific properties
        select = 'displayName,id,mail, userPrincipalName'
        # Get at most 25 results
        top = 25
        # Sort by display name
        order_by = 'displayName'
        request_url = f'{endpoint}?$select={select}&$top={top}&$orderBy={order_by}'

        users_response = self.app_client.get(request_url)
        return users_response.json()


    def createEvent(self, studentName, mentorName, mentorEmail, directorEmail, start_time, end_time, isRecurring, recurringEndDate):
        self.ensure_graph_for_app_only_auth()

        users = self.get_users()['value']

        userId = users[0]['userPrincipalName']

        print(userId)
        #endpoint = '/users/'+userId+'/calendar/events'
        endpoint = '/users/mentor@vbbmentoring.onmicrosoft.com/calendar/events'

        #mentor@vbbmentoring.onmicrosoft.com

        request_url = f'{endpoint}'

        event = {}


        if isRecurring:
            endRecurrDayOfWeek = datetime.datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%S').strftime('%A')

            startRecurrDate = datetime.datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
            endRecurrDate = datetime.datetime.strptime(recurringEndDate,'%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')

            print(endRecurrDayOfWeek)

            event = {
              "subject": "VBB Mentoring Session /w " + studentName,
              "body": {
                "contentType": "HTML",
                "content": "VBB Mentoring Session"
              },
              "start": {
                  "dateTime": start_time,
                  "timeZone": "UTC"
              },
              "end": {
                  "dateTime": end_time,
                  "timeZone": "UTC"
              },
              "location":{
                  "displayName":"MS Calendar Invite."
              },
              "attendees": [
                {
                  "emailAddress": {
                    "address":mentorEmail,
                    "name": mentorName
                  },
                  "type": "required"
                },
                {
                  "emailAddress": {
                    "address":directorEmail,
                  },
                  "type": "required"
                }
              ],
              "recurrence": {
                "pattern": {
                  "type": "weekly",
                  "interval": 1,
                  "daysOfWeek": [ endRecurrDayOfWeek ]

                },
                "range": { "startDate": startRecurrDate, "endDate":endRecurrDate, "type": "endDate" }
              },
              "allowNewTimeProposals": False,
              "isOnlineMeeting": True,
              "onlineMeetingProvider": "teamsForBusiness"
            }
        else:
            event = {
              "subject": "VBB Mentoring Session /w " + studentName,
              "body": {
                "contentType": "HTML",
                "content": "VBB Mentoring Session"
              },
              "start": {
                  "dateTime": start_time,
                  "timeZone": "UTC"
              },
              "end": {
                  "dateTime": end_time,
                  "timeZone": "UTC"
              },
              "location":{
                  "displayName":"MS Calendar Invite."
              },
              "attendees": [
                {
                  "emailAddress": {
                    "address":mentorEmail,
                    "name": mentorName
                  },
                  "type": "required"
                },
                {
                  "emailAddress": {
                    "address":directorEmail,
                  },
                  "type": "required"
                }
              ],
              "allowNewTimeProposals": False,
              "isOnlineMeeting": True,
              "onlineMeetingProvider": "teamsForBusiness"
            }
        print(event)

        jsonPayload = json.dumps(event)
        #print(jsonPayload)

        users_response = self.app_client.post(request_url, data=jsonPayload, headers={'Content-Type': 'application/json'})

        #print(users_response)
        return users_response.json()
