from AppKit import NSWorkspace
import subprocess
import time
import json
import asyncio
from threading import Timer


class AppBlocker:
    def __init__(self, config_path, blacklist = [], whitelist = []):
        self.config_path = config_path
        self.running_apps = []
        self.deamonMode = True
        self.running = True

        self.blacklistActiv = True
        self.blacklist = blacklist
        self.whitelistActiv = False
        self.whitelist = whitelist

    def refresh(self):
        self.running_apps = [apps["NSApplicationName"] for apps in NSWorkspace.sharedWorkspace().launchedApplications()]
        if self.config_path != None:
            self.read_config()

    def read_config(self):
        with open(self.config_path, 'r') as f:
            config = json.load(f)


        self.deamonMode = config['deamonMode']
        self.blacklistActiv = config['blacklistActiv']
        self.whitelistActiv = config['whitelistActiv']
        self.blacklist = config['blacklist']
        self.whitelist = config['whitelist']
        
    def stop_blocking(self):
        self.running = False
        print('- app blocking stopped -')

    def close_app(self, app):
        print(f'Closing: {app}')
        subprocess.call(['osascript', '-e', f'tell application "{app}" to quit'])

    def start_blocking(self):
        print('- start app blocking -')
        while self.running:
            self.refresh()
            time.sleep(1)

            for app in self.running_apps:
                if self.blacklistActiv:
                    if app in self.blacklist:
                        self.close_app(app)
                elif self.whitelistActiv:
                    if not app in self.whitelist:
                        self.close_app(app)

    def custom_session(self, duration):
        timer = Timer(duration, self.stop_blocking)
        timer.start()
        self.start_blocking()
        timer.join()

    def pomodoro(self):
        print('Pomodoro Mode Activated - 25min Intense Focus')
        self.custom_session(25*60)


if __name__ == "__main__":

    config_path = 'config.json'
    appBlocker = AppBlocker(config_path)

    appBlocker.pomodoro()
