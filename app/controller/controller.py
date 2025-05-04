from typing import List, Dict, Any
import json

from app.llm.yandex_gpt import YandexGPT5
from app.config import settings
from app.utils.http_client import grafana_client

def process_request(messages: List[Dict[str, str]]) -> None:
    yandexgpt5 = YandexGPT5(settings.folder_id, auth=settings.yc_api_key)

    result = yandexgpt5.request(messages=messages)

    print(result)

    result_role = result.alternatives[0].role
    result_text = result.alternatives[0].text

    data = json.loads(result_text.replace("```", "").strip())

    response = grafana_client.post("/dashboards/db", data=data)

    if response.status_code == 200:
        print("Dashboard created successfully")
    else:
        print(f"Error creating dashboard: {response.status_code}")

def main() -> None:
    messages = [
        {
            "role": "system",
            "text": "You're DevOps expert. Answer always in JSON format",
        },
        {
            "role": "user",
            "text": "Generate sample JSON dashboard for Grafana HTTP API",
        },
    ]

    process_request(messages)

if __name__ == "__main__":
    main()
