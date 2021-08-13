from AppKit import NSWorkspace
import subprocess
import time
import asyncio
from threading import Timer


class AppBlocker:
    def __init__(self, blacklist, whitelist):
        self.blacklist = blacklist
        self.whitelist = whitelist
        self.running_apps = []
        self.running = True

    def refresh(self):
        self.running_apps = [apps["NSApplicationName"] for apps in NSWorkspace.sharedWorkspace().launchedApplications()]

    def read_config(self, config_path):
        pass #TODO

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
                if app in blacklist:
                    self.close_app(app)

    def custom_session(self, duration):
        timer = Timer(duration, self.stop_blocking)
        timer.start()
        self.start_blocking()
        timer.join()

    def pomodoro(self):
        print('Pomodoro Mode Activated - 25min Intense Focus')
        self.custom_session(25*60)
        

blacklist = ['Brave Browser', 'Twitter', 'WhatsApp', 'Mail']
whitelist = ['Notion', 'Anki', 'Fantastical', 'ToDoist']


if __name__ == '__main__':
    appBlocker = AppBlocker(blacklist, whitelist)
    appBlocker.pomodoro()
