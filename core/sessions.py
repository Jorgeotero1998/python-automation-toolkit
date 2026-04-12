import os
import time
from playwright.sync_api import BrowserContext

class SessionPersistor:
    def __init__(self, storage_dir=".sessions"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_session(self, context: BrowserContext, name: str):
        path = os.path.join(self.storage_dir, f"{name}.json")
        context.storage_state(path=path)
        return path

    def load_session(self, name: str):
        path = os.path.join(self.storage_dir, f"{name}.json")
        if os.path.exists(path):
            # Opcional: Verificar antigüedad del archivo
            return path
        return None
