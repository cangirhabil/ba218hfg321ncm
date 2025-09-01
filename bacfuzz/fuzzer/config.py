import yaml
import os
from datetime import datetime, timedelta

class Config:
    def __init__(self, file_path=None):
        self.start_time = datetime.now()
        self.finish_time = self.start_time + timedelta(hours=8)
        self.file_path = file_path
        self.data = None
        self.homepages = {}
        self.enable_driver = True
        self.enable_checker = True
        self.without_login = False
        self.line_coverage = {}
        self.proxy = None
        self.AIModel = self._select_ai_model() ## Auto-select based on available API keys
        if file_path is not None:
            self.load_config()

    def _select_ai_model(self):
        """
        AI model selection: Priority order Deepseek > Gemini
        Automatic selection based on available environment variables
        """
        deepseek_key = os.getenv('DEEPSEEK_API_KEY')
        gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        if deepseek_key:
            print("[AI CONFIG] Deepseek API key found, Deepseek model selected")
            return "deepseek/deepseek-chat"
        elif gemini_key:
            print("[AI CONFIG] Gemini API key found, Gemini 2.5 Flash model selected")
            return "gemini/gemini-2.5-flash"
        else:
            print("[AI CONFIG] No API key found, defaulting to Deepseek")
            return "deepseek/deepseek-chat"

    def calculate_finish_time(self):
        self.finish_time = self.start_time + timedelta(hours=self.data['RUNNING_TIME']['h'],minutes=self.data['RUNNING_TIME']['m'])

    def load_config(self, file_path=None):
        if file_path is not None:
            self.file_path = file_path

        with open(self.file_path, encoding="utf-8_sig") as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)
        print(f'A config file from {self.file_path} is loaded.')

config = Config()

if __name__ == "__main__":
    config = Config(file_path="../configs/config-xvwa.yaml")
    print(config.data['UNIQUE_STRING'])