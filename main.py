from PyQt6.QtWidgets import (QApplication, 
                             QFileDialog,
                             QWidget)

from PyQt6.QtGui import     (QCloseEvent,
                             QColor)

from PyQt6 import           uic

#concrete watcher (implementation of abstract class)
from watcher.watcher import ResourceWatcher

from datetime import datetime
import sys, os

#strategies
from strategies.strategyadding import AddingStrategy
from strategies.strategyremoving import RemovingStrategy
from strategies.strategyrenaming import RenamingStrategy
from strategies.strategyresezing import ResizingStrategy

class Window( QWidget ):

    def __init__(self):
        super(Window, self).__init__()

        uic.loadUi( "ui/watcher_ui.ui", self )

        #code logic here ...
        self.resource = ResourceWatcher()

        #adding strategy
        self.resource.add_resource_strategy( AddingStrategy() )
        self.resource.add_resource_strategy( RemovingStrategy() )
        self.resource.add_resource_strategy( RenamingStrategy() )
        self.resource.add_resource_strategy( ResizingStrategy() )

        #conencting signals

        self.open_directory_btn.clicked.connect( self.open_directory )
        
        self.resource.on_resource.connect( self.handle_event )

        self.interval_input.valueChanged.connect( self.handle_interval )

    def open_directory(self) -> None:

        home_dir = os.path.expanduser('~')

        folder_path = QFileDialog.getExistingDirectory(self, 'Select Directory', home_dir)

        if folder_path:

            self.resource.set_attributes(directory=folder_path)
            
            self.path_edit.setText( folder_path )

            #if it was text before, then clear it
            if self.area_text.toPlainText() != '':
                self.area_text.clear()

            if self.resource.is_watching():
                self.resource.stop_watching()

            self.resource.start_watching()
            # self.resource._event.set()

            #setting some text5 to warn user
            self.status_lbl.setText('Watching ...')

    def deamon_thread(self):

        pass
        # self.monitor.start_explicit()

        #dissabeling interval input ui element/spinner
        # self.interval_input.setEnabled(False)

    def handle_event(self, resource: dict) -> None:
        extra = resource.get('extra')

        text: str = str()
        reason: str = str()

        action_type = resource.get('action_type')

        if action_type == 'Adding':
            reason = f' was added to {resource.get("path")} '
            self.area_text.setTextColor(QColor('lightblue'))

        if action_type == 'Removing':
            reason = f' was/were removed from {resource.get("path")} '
            self.area_text.setTextColor(QColor('red'))

        if action_type == 'Renaming':
            reason = f' was renamed in {resource.get("path")} '
            self.area_text.setTextColor(QColor('yellow'))

        if action_type == 'Resizing':
            reason = f' was modified in {resource.get("path")} '
            self.area_text.setTextColor(QColor('white'))

        for ex in extra:
            now_time_format = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            text = f'{ex.get("name")} {reason} -> size: {ex.get("size")} -> {now_time_format}\n\n'
                    
            self.area_text.append( text )
        
    def handle_interval(self, value) -> None:
        # print('chanign to ', value)
        self.resource.set_attributes(interval=value)

    def closeEvent(self, event: QCloseEvent):
        if self.resource.is_watching():
            self.resource.stop_watching()

            event.accept()



if __name__ == "__main__":

    app = QApplication( sys.argv )

    # app.setStyle('Fusion')

    window = Window()

    window.show()

    app.exec()