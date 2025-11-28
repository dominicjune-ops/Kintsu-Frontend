import os
import requests

def send_slack_message(channel, message):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL environment variable is not set.")

    payload = {
        "channel": channel,
        "text": message
    }

    response = requests.post(webhook_url, json=payload)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is: {response.text}")

if __name__ == "__main__":
    # Example usage
    send_slack_message("#project-updates", "Daily report: All tasks are on track.")