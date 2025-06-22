import re, json, os

from app.config.grafana_config import grafana_settings
from app.config.logging_config import logger
from typing import Dict, Any


# Записывает JSON строку в файл
def write_json_str_to_file(json_str: str, file_name):
    сurrent_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(сurrent_dir, file_name)
    try:
        jsn = json.loads(json_str)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(jsn, f)
    except Exception as error:
        print(error)


# Записывает обычную строку в файл
def write_str_to_file(str: str, file_name):
    сurrent_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(сurrent_dir, file_name)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str)
    except Exception as error:
        print(error)


# Извлекает, валидирует и исправляет JSON для соответствия требованиям Grafana
def extract_json_from_response(response: str) -> Dict[str, Any]:
    """Извлекает и валидирует JSON из ответа LLM, обрабатывая поле id"""
    try:
        response = remove_markdown(response)
        response = fix_inner_quotes(response)
        parsed_json = json.loads(response)

        # Проверяем наличие dashboard в корне
        if 'dashboard' not in parsed_json:
            if any(key in parsed_json for key in ['panels', 'title', 'schemaVersion']):
                parsed_json = {'dashboard': parsed_json}
            else:
                raise ValueError("Response doesn't contain valid Grafana dashboard structure")

        # Удаляем id из корня дашборда, если он есть
        if 'id' in parsed_json['dashboard']:
            del parsed_json['dashboard']['id']

        # Добавляем обязательные поля
        parsed_json['folderId'] = 0
        parsed_json['overwrite'] = True
        parsed_json['uid'] = grafana_settings.dashboard_uid

        return parsed_json

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}\nResponse: {response[:500]}")
        raise RuntimeError(f"Invalid JSON from LLM: {str(e)}")
    except ValueError as e:
        logger.error(f"Dashboard validation failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise RuntimeError(f"Failed to process LLM response: {str(e)}")


# удаляет разметку markdown ```json ... ```
def remove_markdown(response):
    response = re.sub(r'^```(json)?|```$', '', response, flags=re.MULTILINE).strip()
    return response


# Исправляет кавычки в выражениях типа expr
def fix_inner_quotes(json_str: str) -> str:
    """Исправляет кавычки в выражениях типа expr"""
    # Ищем все вхождения "expr": "..." и экранируем внутренние кавычки
    return re.sub(
        r'("expr"\s*:\s*)"([^"]*)"',
        lambda m: f'{m.group(1)}"{m.group(2).replace('"', r'\"')}"',
        json_str
    )
