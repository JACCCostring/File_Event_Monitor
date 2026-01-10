from abc import             (ABC, 
                             abstractmethod)

from typing import          List

class IResourceStrategy( ABC ):

    def __init__(self):
        super().__init__()
    
        # self.resources: List[ os.DirEntry ] = []
        # self.action_type: ActionType = None

    @abstractmethod
    def action_strategy(self, current_resources: List[ str ], last_seen_resources: List[ str ], directory: str) -> bool:
        '''
        Docstring for action_strategy
        
        :param current_resources: list of all current name resources of a directory
        :param last_seen_resources: list of all last seen name resources of a directory
        and only return true if satisfied
        '''

        return NotImplemented