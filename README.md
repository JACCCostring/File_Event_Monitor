<h1> File Event Watcher </h1>

<b> An Object Oriented approach to file or folder events monitoring or watcher, from Create, Remove, name changing or size modifications and just for fun :) </b>

the code is thought taking in account some OOP principles like Polimorphysm, Observer design pattern and close for modification but open for extension.

meaning that developer can extent the code as much as it can be extended. Just by adding new strategies (it's how i call it, any event developer want to handle like creation or deletion of a file or folder). Of course developer must inherit or subclass IResourceStrategy and add it to the concrate class of IResourceWatcher.

Example of use:

```python

#where we have Adding Strategy -> this strat.. is when files/folders are created
from strategies.strategyadding import AddingStrategy

#where we have IResourceStrategy this is our interface or abstract class to create any strategy
from strategies.resourcestrategy import IResourceStrategy

#subclassing IResourceWatcher
class ConcreteWatcher( IResourceWatcher ):
    def __init__(self):
        super().__init__()

    #just overriding on_notify abstract method
    def on_notify(self, resource: IResourceStrategy):
        pass

def main():

    '''
    attribs by default are:
        directory='.' current or parent directory
        interval=1.0
        ActionType=ActionType.Adding -> this is an enum class with possible Actions for events
    '''

    watcher = ConcreteWatcher()

    watcher.set_attributes()

    watcher.add_resource_strategy( AddingStrategy() )

    watcher.start_watching()

    #also developer can see when watcher/monitor is running consulting is_watching() method

    #to stop the watcher/monitor just use the method stop_watching() or watcher.stop_watching()

```

Example:

<img width="1678" height="978" alt="Screenshot 2026-01-22 at 19 09 54" src="https://github.com/user-attachments/assets/bab7e8c9-1c9e-41fc-b26c-f16d132e2e20" />

<img width="953" height="980" alt="Screenshot 2026-01-22 at 19 10 24" src="https://github.com/user-attachments/assets/f972a8ad-7210-455f-92dc-c1c9e3970416" />

