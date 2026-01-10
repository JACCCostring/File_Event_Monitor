# from resourcestrategy import IResourceStrategy

from strategies.resourcestrategy import IResourceStrategy

from watcher.watchertypes import ActionType

from typing import List

import os

class AddingStrategy(IResourceStrategy):
    def __init__(self):
        super().__init__()

        self.resources: List[os.DirEntry] = []
        self.action_type: ActionType = ActionType.Adding
        self.path: str = str()

    def action_strategy(self, current_resources, last_seen_resources, directory):
        size_current: int = len( current_resources )
        size_last_seen:int = len( last_seen_resources )

        self.path = directory

        def get_added_resources() -> List[os.DirEntry]:
            last_names: List[str] = []
            missing_resources: list[os.DirEntry] = []

            for last_entry in last_seen_resources:
                last_names.append(last_entry.name)
            
            for current_entry in current_resources:
                if current_entry.name not in last_names:
                    missing_resources.append(current_entry)
        
            return missing_resources
    
        if size_current > size_last_seen:
            self.resources = get_added_resources()
            # print('added', self.resources)
            return True