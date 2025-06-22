from app.llm_clients import BaseLLMClient, LLM_Response
from .functions import *
from ..grafana.client import grafana_client


class AIAgent:
    def __init__(self, llm_client: BaseLLMClient):
        self.llm_client = llm_client
        self.grafana_client = grafana_client

    def process_command(self, user_prompt):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'system_prompt.txt')
        with open(file_path, "+r", encoding='utf-8') as file:
            system_prompt = file.read()
        logger.info("=" * 30 + "Model: " + self.llm_client.model + "=" * 30)
        logger.info("user_prompt: " + user_prompt)
        extended_user_prompt = self.preprocess(user_prompt)
        llm_response = self.ask_llm(extended_user_prompt, system_prompt)
        if llm_response.http_status != 200:
            logger.info(f'LLM вернула ошибку (код {llm_response.http_status}): {llm_response.error}')
            return f'LLM вернула ошибку (код {llm_response.http_status}): {llm_response.error}'
        try:
            logger.info(f'Ответ от LLM получен. Использовано токенов: {llm_response.tokens}')
            llm_response = self.postprocess(llm_response)
            write_json_str_to_file(llm_response.answer, 'response.json')
            grafana_client.update_dashboard(llm_response.answer)
            return "Команда обработана успешно"
        except Exception as error:
            write_str_to_file(llm_response.answer)
            logger.info(f'Возникла ошибка при обработке ответа LLM: {error}')
            return f'Возникла ошибка при обработке ответа LLM: {error}'

    def preprocess(self, user_prompt: str):
        dashboard = grafana_client.get_dashboard(grafana_settings.dashboard_uid)
        user_prompt += "\n" + "в качестве основы используй дашборд " + json.dumps(dashboard)
        return user_prompt

    def ask_llm(self, user_prompt: str, system_prompt) -> LLM_Response:
        answer = self.llm_client.ask_assistant(user_prompt, system_prompt)
        return answer

    def postprocess(self, llm_response: LLM_Response):
        llm_response.answer = extract_json_from_response(llm_response.answer)
        return llm_response
