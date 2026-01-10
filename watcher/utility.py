from typing import (List)
import os

class ConfigResource:
    def __init__(self):
        pass
    
    @classmethod
    def get_resources(self, instances: bool, directory: str):
        content: List[ os.DirEntry ] = []

        with os.scandir( directory ) as entries:
            for entry in entries:
                content.append( entry )

        if instances:

            return content
        
        names = [entry.name for entry in content]

        return names