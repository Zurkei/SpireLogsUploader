import os
import shutil
import configparser
from spire_log_wrapper import SpireLogWrapper
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

spire_log = SpireLogWrapper()


class ConfigLoader:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.game_dir = self.config['DEFAULT']['GameDirectory']
        self.run_dir = self.game_dir + 'runs/'
        self.uploaded_dir = self.run_dir + 'UPLOADED/'

    def correct_config(self):
        return os.path.exists(self.game_dir)


class SpireLogUploader:
    def __init__(self):
        self.config = ConfigLoader()

    @staticmethod
    def login(username, password):
        return spire_log.login(username, password)

    def start_watch(self):
        self.observer = Observer()
        self.event_handler = self.Handler()
        self.event_handler.load_spire_uploader(self)
        self.observer.schedule(self.event_handler, self.config.run_dir, recursive=True)
        self.observer.start()

    def stop_watch(self):
        self.observer.stop()

    def move_log(self, file):
        if not os.path.exists(self.config.uploaded_dir):
            os.makedirs(self.config.uploaded_dir)
        file_name = file.split("\\")[-1]
        if not os.path.exists(self.config.uploaded_dir + file_name):
            shutil.move(file, self.config.uploaded_dir)
        else:
            print(f'{file_name} exists already in upload directory')

    def upload_run(self, file):
        if 'UPLOADED' in file or 'DAILY' in file:
            return
        file_name = file.split('\\')[-1]
        if spire_log.upload_run(file):
            print(f'Uploaded {file_name} successfully')
            self.move_log(file)
        else:
            print(f'Unable to upload {file_name}')

    def upload_all(self):
        for root, dirs, files in os.walk(self.config.run_dir):
            for current_dir in dirs:
                if 'UPLOADED' in current_dir or 'DAILY' in current_dir:
                    continue
                current_dir = os.path.join(root, current_dir)
                for r2, d2, f2 in os.walk(current_dir):
                    for file in f2:
                        self.upload_run(os.path.join(current_dir, file))

    class Handler(FileSystemEventHandler):
        def load_spire_uploader(self, spire_log_uploader):
            self.spire_log_uploader = spire_log_uploader

        def on_created(self, event):
            if event.is_directory:
                return None
            else:
                self.spire_log_uploader.upload_run(event.src_path)
