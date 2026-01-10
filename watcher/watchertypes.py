from enum import Enum

class ActionType(int, Enum):
    Adding = 0
    Removing = 1
    Renaming = 2
    Resizing = 3

class ResourceType(int, Enum):
    FileType = 0
    FolderType = 1
