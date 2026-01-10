# from resourcestrategy import IResourceStrategy

from strategies.resourcestrategy import IResourceStrategy

from watcher.watchertypes import ActionType

from typing import List, Dict

import os


class ResizingStrategy(IResourceStrategy):
    def __init__(self):
        super().__init__()

        self.resources: List[os.DirEntry] = []
        self.action_type: ActionType = ActionType.Resizing

        self.path: str = str()

    def action_strategy(self, current_resources, last_seen_resources, directory):
        # size_current:int = len( current_resources )
        # size_last_seen:int = len( last_seen_resources )
        current_stats: List[Dict[str, str]] = []
        last_stats: List[Dict[str, str]] = []
        entries: List[os.DirEntry] = []
        stats: list[str] = []

        kb: int = 1000 #to divide in kilobytes

        self.path = directory

        def check_if_size_changed() -> List[str]:
            for entry_current in current_resources:
                current_stats.append({'name': entry_current.name, 'size': entry_current.stat().st_size / kb})
            
            for entry_last in last_seen_resources:
                last_stats.append({'name': entry_last.name, 'size': entry_last.stat().st_size / kb})

            for c_stat in current_stats:
                for l_stat in last_stats:
                    if c_stat.get('name') == l_stat.get('name'):
                        if c_stat.get('size') > l_stat.get('size') or c_stat.get('size') < l_stat.get('size'):
                            stats.append(c_stat.get('name'))
            
            #get instances according to name, it's what we need
            for entry in current_resources:
                for entry_name in stats:
                    if entry_name == entry.name:
                        entries.append(entry)
            
            len_entries: int = len(entries)

            if len_entries > 0:
                self.resources = entries.copy()

            return len_entries > 0
        

        if check_if_size_changed():

            return True