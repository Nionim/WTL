import time, os, jsonreader as jr
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import filetransfer as action
import threading

transferedFilesDir = jr.getData("Main-Dir")

class changeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file = event.src_path
            remote_path = jr.getData(file)
            if remote_path: action.editFile(file, remote_path)
            else: print(f"{file} not found in Json")
            
#    def on_created(self, event):
#        if not event.is_directory:
#            file = event.src_path
#            action.editFile(file, getNormalPath(file))

    def on_deleted(self, event):
        if not event.is_directory:
            file = event.src_path
            remote_path = jr.getData(file)
            if remote_path: action.deleteFile(remote_path)
            else: print(f"{file} not found in Json")

def getNormalPath(path):
    return os.path.relpath(path, transferedFilesDir)

def onInitCommands():
    commands = jr.getCommands()
    for c in commands:
        action.runCommand(c)

if __name__ == "__main__":
    #onInitCommands()
    handler = changeHandler()
    observer = Observer()
    observer.schedule(handler, transferedFilesDir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()