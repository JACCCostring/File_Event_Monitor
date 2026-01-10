# from resourcestrategy import    IResourceStrategy
from strategies.resourcestrategy import IResourceStrategy

from watcher.watchertypes import        ActionType

from typing import              List

import                          os



class RemovingStrategy(IResourceStrategy):
    def __init__(self):
        super().__init__()

        self.resources: List[os.DirEntry] = []
        self.action_type: ActionType = ActionType.Removing

        self.path: str = str()

    def action_strategy(self, current_resources, last_seen_resources, directory):
        size_current:int = len( current_resources )
        size_last_seen:int = len( last_seen_resources )
        
        self.path = directory

        def get_removed_resources() -> List[os.DirEntry]:
            current_names: List[str] = []
            missing_resources: list[os.DirEntry] = []

            for current_entry in current_resources:
                current_names.append(current_entry.name)
            
            for last_entry in last_seen_resources:
                if last_entry.name not in current_names:
                    missing_resources.append(last_entry)
            
            return missing_resources
    
        if size_current < size_last_seen:
            self.resources = get_removed_resources()
            return True