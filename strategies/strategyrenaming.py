# from resourcestrategy import IResourceStrategy

from strategies.resourcestrategy import IResourceStrategy

from watcher.watchertypes import ActionType

from typing import List

import os

class RenamingStrategy(IResourceStrategy):
    def __init__(self):
        super().__init__()

        self.resources: List[os.DirEntry] = []
        self.action_type: ActionType = ActionType.Renaming

        self.path: str = str()

    def action_strategy(self, current_resources, last_seen_resources, directory):
        size_current:int = len( current_resources )
        size_last_seen:int = len( last_seen_resources )

        self.path = directory

        def check_if_any_name_changes() -> bool:
            names: List[str] = []
            renames: List[os.DirEntry] = []
            new_names: List[os.DirEntry] = []

            for entry in current_resources:
                names.append(entry.name)

            for entry in last_seen_resources:
                if entry.name not in names:
                    if size_current == size_last_seen:
                        renames.append(entry)
            
            if len(renames) > 0:
                self.resources = renames.copy()
                return True
            
            return False


        if check_if_any_name_changes():
            # print('renamed: ', self.resources)
            return True