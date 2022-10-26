import json
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from msgraph.core import GraphClient

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
        select = 'displayName,id,mail'
        # Get at most 25 results
        top = 25
        # Sort by display name
        order_by = 'displayName'
        request_url = f'{endpoint}?$select={select}&$top={top}&$orderBy={order_by}'

        users_response = self.app_client.get(request_url)
        return users_response.json()


    def createEvent(self, mentorName, mentorEmail, directorEmail, start_time, end_time, calendar_id, isRecurring, recurringEndDate=None):
        self.ensure_graph_for_app_only_auth()
        endpoint = '/me/events'

        request_url = f'{endpoint}'

        if isRecurring:
            event = {
              "subject": "Test Calendar",
              "body": {
                "contentType": "HTML",
                "content": "Does this time work for you?"
              },
              "start": {
                  "dateTime": start_time,
                  "timeZone": "Pacific Standard Time"
              },
              "end": {
                  "dateTime": end_time,
                  "timeZone": "Pacific Standard Time"
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
                }
              ],
              "recurrence": {
                "pattern": {
                  "type": "weekly",
                  "interval": 1,
                  "daysOfWeek": [ "Thursday" ]
                },
                "range": { "startDate": start_time, "endDate":recurringEndDate, "type": "endDate" }
              },
              "allowNewTimeProposals": True,
              "isOnlineMeeting": False,
              "onlineMeetingProvider": "teamsForBusiness"
            }
        else:
            event = {
              "subject": "Test Calendar",
              "body": {
                "contentType": "HTML",
                "content": "Does this time work for you?"
              },
              "start": {
                  "dateTime": start_time,
                  "timeZone": "Pacific Standard Time"
              },
              "end": {
                  "dateTime": end_time,
                  "timeZone": "Pacific Standard Time"
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
                }
              ],
              "allowNewTimeProposals": True,
              "isOnlineMeeting": False,
              "onlineMeetingProvider": "teamsForBusiness"
            }


        users_response = self.app_client.api(request_url).post(event)
        return users_response.json()
