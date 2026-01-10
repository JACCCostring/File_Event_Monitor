import pytest
import sys, os #for os.path and sys.path

'''
what's suposed to be a normal import, but sometimes pytest or python module manager
can not find modules
'''
# from watcher.resourcewatcher import IResourceWatcher

try:

    from watcher.resourcewatcher import IResourceWatcher

except ModuleNotFoundError:

    abs = os.path.curdir

    sys.path.append(abs)
    
    from watcher.resourcewatcher import IResourceWatcher
    from strategies.strategyadding import AddingStrategy
    from strategies.resourcestrategy import IResourceStrategy

#subclassing IResourceWatcher
class ResourceInstance( IResourceWatcher ):
    def __init__(self):
        super().__init__()
    
    #just overriding on_notify abstract method
    def on_notify(self, resource: IResourceStrategy):
        pass

@pytest.fixture
def resource_instance() -> IResourceWatcher:
    return ResourceInstance()

def test_if_is_not_watching( resource_instance ):

    assert not resource_instance.is_watching()

def test_if_is_watching_without_attribs( resource_instance ):

    # resource_instance.set_attributes()

    resource_instance.add_resource_strategy(AddingStrategy())

    resource_instance.start_watching()

    assert not resource_instance.is_watching()

def test_if_is_watching_with_attribs( resource_instance ):

    resource_instance.set_attributes()

    resource_instance.add_resource_strategy(AddingStrategy())

    resource_instance.start_watching()

    assert resource_instance.is_watching()

    resource_instance.stop_watching()

def test_if_watching_can_stop( resource_instance ):

    resource_instance.set_attributes()

    resource_instance.add_resource_strategy(AddingStrategy())

    resource_instance.start_watching()

    if resource_instance.is_watching():

        resource_instance.stop_watching()

    assert not resource_instance.is_watching()


def test_if_attribs_are_not_set( resource_instance ):

    assert not resource_instance.is_attrbs_set()

def test_if_attribs_are_set( resource_instance ):

    resource_instance.set_attributes()

    assert resource_instance.is_attrbs_set()
