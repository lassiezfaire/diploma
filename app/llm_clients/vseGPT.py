import os
from dotenv import load_dotenv

from .BaseLLM import BaseLLMClient, LLM_Response

load_dotenv()


class VseGPT(BaseLLMClient):

    def __init__(self):
        self.api_key = os.getenv("VSGPT_API_KEY")
        self.model = 'deepseek/deepseek-chat-0324-alt-fast'
        self.base_headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }

    def _ask_llm_api(self, user_prompt: str, system_prompt=None) -> LLM_Response:
        url = 'https://api.vsegpt.ru/v1/chat/completions'
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        response = self._post_request(url, payload)
        payload = response.json()
        if response.status_code == 200:
            result = LLM_Response(http_status=200, answer=payload["choices"][0]["message"]["content"],
                                  tokens=payload['usage']['total_tokens'])
        else:
            result = LLM_Response(http_status=response.status_code, error="", tokens=0)
        return result
