import json
from datetime import datetime

class Memory:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load()

    def _load(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"conversations": []}

    def save(self, user_input, response):
        self.data["conversations"].append({
            "input": user_input,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=2)