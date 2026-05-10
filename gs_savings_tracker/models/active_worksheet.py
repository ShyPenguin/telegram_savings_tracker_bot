from pathlib import Path
import json
import os
from .worksheet import Worksheet

class ActiveWorksheet(Worksheet):

    CACHE_PATH = Path(os.path.join(os.getcwd(), "cache/active_worksheet.json"))
    
    def __init__(self, title="", id=""): 
        super().__init__(title, id)
        
    def has_cache(self) -> bool:
        return self.title != "" or self.id != ""
        
    def save(self):
        data = {
            "title": self.title,
            "id": self.id
        }

        with open(self.CACHE_PATH, "w") as file:
            json.dump(data, file)

    @classmethod
    def load(cls):

        if not cls.CACHE_PATH.exists():

            cls.CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

            data = {
                "title": "",
                "id": ""
            }

            with open(cls.CACHE_PATH, "w") as file:
                json.dump(data, file, indent=4)
            return cls(**data)

        with open(cls.CACHE_PATH, "r") as file:
            data = json.load(file)

        return cls(**data)
    
    def set(self, title, id):
        self.title = title
        self.id = id
        self.save()