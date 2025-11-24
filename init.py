import time, os, jsonreader as jr
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import filetransfer as action

transferedFilesDir = jr.getData("Main-Dir")

class changeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file = event.src_path
            action.editFile(file, getNormalPath(file))

#    def on_created(self, event):
#        if not event.is_directory:
#            file = event.src_path
#            action.editFile(file, getNormalPath(file))

    def on_deleted(self, event):
        if not event.is_directory:
            file = event.src_path
            action.deleteFile(getNormalPath(file))

def getNormalPath(path):
    return os.path.relpath(path, transferedFilesDir)

if __name__ == "__main__":
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