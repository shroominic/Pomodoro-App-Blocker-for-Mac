from AppKit import NSWorkspace
import subprocess
import time

class AppBlocker:
    def __init__(self, blacklist, whitelist):
        self.blacklist = blacklist
        self.whitelist = whitelist
        self.running_apps = []
        self.running = True

    def refresh(self):
        self.running_apps = [apps["NSApplicationName"] for apps in NSWorkspace.sharedWorkspace().launchedApplications()]

    def close_app(self, app):
        subprocess.call(['osascript', '-e', f'tell application "{app}" to quit'])

    def start_blocking(self):
        while self.running:
    
            self.refresh()
            time.sleep(1)

            for app in self.running_apps:
                if app in blacklist:
                    print(app)
                    self.close_app(app)



blacklist = ['Brave Browser', 'Safari', 'Twitter', 'WhatsApp']
whitelist = ['Notion', 'Anki', 'Fantastical', 'ToDoist']

if __name__ == '__main__':
    appBlocker = AppBlocker(blacklist, whitelist)
    appBlocker.start_blocking()
