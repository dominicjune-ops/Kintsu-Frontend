import requests
import os

def update_notion_page(page_id, content):
    notion_token = os.getenv("NOTION_API_TOKEN")
    if not notion_token:
        raise ValueError("NOTION_API_TOKEN environment variable is not set.")

    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    payload = {
        "properties": {
            "Content": {
                "rich_text": [
                    {
                        "text": {
                            "content": content
                        }
                    }
                ]
            }
        }
    }

    response = requests.patch(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Request to Notion returned an error {response.status_code}, the response is: {response.text}")

if __name__ == "__main__":
    # Example usage
    update_notion_page("your-page-id", "Daily report: All tasks are on track.")