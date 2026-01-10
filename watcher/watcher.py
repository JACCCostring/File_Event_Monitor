from strategies.resourcestrategy import IResourceStrategy
from watcher.resourcewatcher import IResourceWatcher
from watcher.watchertypes import ActionType

from PyQt6.QtCore import    (QObject, 
                             pyqtSignal)

from typing import (List,
                    Dict)

from abc import ABCMeta

# a combined metaclass
class CombinedMeta(type(QObject), ABCMeta):
    pass

class ResourceWatcher(QObject, IResourceWatcher, metaclass=CombinedMeta):
    def __init__(self):
        super().__init__()

    # on_resource = pyqtSignal(IResourceStrategy)
    on_resource = pyqtSignal( dict )

    def on_notify(self, resource: IResourceStrategy):
        extra: List[Dict[str, str]] = []
        action_type: str = str()

        for s in resource.resources:
            extra.append( {'name': s.name, 'size': s.stat().st_size / 1000} )
        
            if resource.action_type == ActionType.Adding:
                action_type = 'Adding'
            if resource.action_type == ActionType.Removing:
                action_type = 'Removing'
            if resource.action_type == ActionType.Renaming:
                action_type = 'Renaming'
            if resource.action_type == ActionType.Resizing:
                action_type = 'Resizing'

        self.on_resource.emit( {'extra': extra, 'action_type': action_type, 'path': resource.path} )