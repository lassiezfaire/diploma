from typing import Dict, Any, List
import json
import os

# класс позволяет сохранять значения переменных между запусками программы

class SessionManager:

    def __init__(self, session_id: str = 'defaultsession'):
        self.set_session_id(session_id)

    def set_session_id(self, session_id):
        self._session_id = session_id
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self._file_name = os.path.join(script_dir, self._session_id + '.json')
        self.session: Dict[str, any] = self.update_from_file()

    def set(self, name, value):
        self.session[name] = value
        with open(self._file_name, 'w', encoding='utf-8') as file:
            json.dump(self.session, file, ensure_ascii=False, indent=4)

    def get(self, name: str, default = None) -> any:
        if name in self.session:
            return self.session[name]
        else:
            return default

    def update_from_file(self):
        try:
            with open(self._file_name, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

