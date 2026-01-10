from abc import             (ABC, 
                             ABCMeta, 
                             abstractmethod)

from typing import          (List)

from strategies.resourcestrategy import IResourceStrategy

from watcher.utility import ConfigResource

from watcher.watchertypes import (ActionType, 
                          ResourceType)

import                      threading
import                      time
import                      os



class IResourceWatcher( ABC ):

    def __init__(self):
        super().__init__()
        
        #threads for watching in a loop and keep notifying
        self._watcher_thread = threading.Thread(target=self._watching_method, args=[])
        self._notify_thread = threading.Thread(target=self._notify, args=[])

        #event thread for sincrhronization
        self._event = threading.Event()

        self._is_watching: bool = False #for running watcher lopp
        self._is_warning: bool = False #for running notifier loop

        #list of IResources
        self._resource_strategies: List[ IResourceStrategy ] = []

        #action type and resource type
        self._action_type: ActionType = None
        self._resource_type: ResourceType = None
        self._directory: str = None

        #after atrribs are set, then only we can start watching
        self._is_attrib_ready: bool = False

        #current and last seen directory resources
        self._current_resources: List[ os.DirEntry ]
        self._last_seen_resources: List[ os.DirEntry ]

        #interval for watcher thread
        self._interval: float = 1.0 #default value
    
    def add_resource_strategy(self, resource_strategy: IResourceStrategy) -> None:
        if resource_strategy:

            self._resource_strategies.append( resource_strategy )

    def set_attributes(self, action: ActionType = ActionType.Adding,  
                       directory: str = str('.'), interval: float = 1.0) -> None:
        
        self._action_type = action
        # self._resource_type = resource_type
        self._directory = directory
        self._interval = interval

        self._is_attrib_ready = True
    
    def start_watching(self) -> None:
        if not self._watcher_thread.is_alive() and self._is_attrib_ready:
            try:
                
                self._is_watching = True #we turn watcher flag to true

                self._init_resources() #to init.. last seen resources at start of thread

                self._watcher_thread.start() #we start the watcher thread
                self._notify_thread.start() #we start the notifier thread

            except RuntimeError as msg:

                print(msg)

    def _init_resources(self) -> None:
        self._last_seen_resources = ConfigResource.get_resources( instances=True, directory=self._directory )

    def stop_watching(self) -> None:
        if self._is_watching:
            self._is_watching = False

            self._is_attrib_ready = False

            #wake up waiting warn thread again, to release it, before joining warn thread
            self._wake()

            self._watcher_thread.join()
            self._notify_thread.join()
    
    def is_watching(self) -> bool:
        return self._is_watching
    
    def is_attrbs_set(self) -> bool:
        return self._is_attrib_ready
    
    def _wake(self) -> None:
        if self._watcher_thread.is_alive():
            self._event.set()

    def _watching_method(self) -> None:
        
        # print('watching ...')

        while self._is_watching:
            for strategy in self._resource_strategies:
                current_resources = ConfigResource.get_resources(instances=True, directory=self._directory)
                if strategy.action_strategy(current_resources, self._last_seen_resources, directory=self._directory):
                    #wake up thread
                    self._wake()

            time.sleep( self._interval )

    def _notify(self) -> None:
        while self._is_watching:
            self._event.wait()

            #re-init resources again to initialise self._last_seen_resources content
            self._init_resources()

            #we need to notify of any action type
            for strategy in self._resource_strategies:
                if strategy:
                    if len(strategy.resources) > 0:
                        self.on_notify( strategy )

                        #clearing resources, to have new session on each iteration when watching resources
                        strategy.resources.clear()

            #clear event thread/s to put it in waiting state again
            self._event.clear()

    @abstractmethod
    def on_notify(self, resource: IResourceStrategy) -> None:
        pass