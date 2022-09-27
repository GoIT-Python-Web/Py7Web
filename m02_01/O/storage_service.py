from __future__ import annotations

from storage import *


class StorageService:
    def __init__(self, storage: JSONStorage | YamlStorage):
        self.storage = storage

    def get(self, key: str) -> str:
        return self.storage.get_value(key)


# storage = StorageService(JSONStorage('data.json'))
storage = StorageService(YamlStorage('data.yaml'))
print(storage.get('username'))
