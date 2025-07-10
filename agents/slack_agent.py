import requests

class SlackAgent:
    def __init__(self):
        self.webhook_url = ""

    def handle(self, message: str, user_id: str) -> str:
        self.send_to_slack(message, user_id)
        return "I've contacted our human support team on Slack. Someone will reach out to you shortly!"

    def send_to_slack(self, message: str, user_id: str):

        #Protótipo para redirecionamento via webhook
        '''
        content = f"New Ticket from User: {user_id}\nMessage: {message}"
        requests.post(self.webhook_url, json={"content": content})
        '''

        print(f"[SlackAgent] Requesting human help for '{user_id}' with the message: {message}")
