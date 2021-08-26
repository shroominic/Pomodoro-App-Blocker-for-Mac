from AppKit import NSWorkspace
import subprocess
import rumps
import json

class AppBlocker(object):
    def __init__(self):
        self.config = {
            "app_name": "Pomodoro Blocker",
            "whitelist": ["Visual Studio Code"],
            "blockedSites": ["youtube.com", "instagram.com"],
            "blacklist": ["Twitter", "WhatsApp", "Mail", "Minecraft"],
            "break_message": "Time is up! Take a break :)",
            "continue": "Continue Timer",
            "start": "Start Timer",
            "pause": "Pause Timer",
            "stop": "Stop Timer",
            "blacklistActiv": "True",
            "whitelistActiv": "False",
            "deamonMode": "False",
            "interval": 1500, }
        self.app = rumps.App(self.config["app_name"], "🍅")
        self.timer = rumps.Timer(self.on_tick, 1)
        self.interval = self.config["interval"]
        self.running_apps = []
        
        self.set_up_menu()
        self.start_pause_button = rumps.MenuItem(title=self.config["start"], callback=self.start_timer)
        self.app.menu = [self.start_pause_button]

        self.blacklist = self.config["blacklist"]
        self.whitelist = self.config["whitelist"]
        self.blockedSites = self.config["blockedSites"]
        self.blacklistActiv = self.config["blacklistActiv"]
        self.whitelistActiv = self.config["whitelistActiv"]

    def change_interval(self, interval):
        self.interval = interval

    def write_config(self):
        with open('config.json', 'w') as fp:
            json.dump(self.config, fp)

    def read_config(self):
        print('') # TODO

    def close_app(self, app):
        print(f'Closing: {app}')
        subprocess.call(['osascript', '-e', f'tell application "{app}" to quit'])
    
    def set_up_menu(self):
        self.timer.stop()
        self.timer.count = 0
        self.app.title = "🍅"
        self.write_config()

    def on_tick(self, sender):
        time_left = sender.end - sender.count
        mins = time_left // 60 if time_left >= 0 else time_left // 60 + 1
        secs = time_left % 60 if time_left >= 0 else (-1 * time_left) % 60
        
        self.running_apps = [apps["NSApplicationName"] for apps in NSWorkspace.sharedWorkspace().launchedApplications()]
        for app in self.running_apps:
                if self.blacklistActiv:
                    if app in self.blacklist:
                        self.close_app(app)
                elif self.whitelistActiv:
                    if not app in self.whitelist:
                        self.close_app(app)

        if mins == 0 and time_left < 0:
            rumps.notification(title=self.config["app_name"], subtitle=self.config["break_message"], message='')
            self.stop_timer()
        else:
            self.app.title = '{:2d}:{:02d}'.format(mins, secs)

        sender.count += 1

    def start_timer(self, sender):
        if sender.title.lower().startswith(("start", "continue")):
            if sender.title == self.config["start"]:
                self.timer.count = 0
                self.timer.end = self.interval
            sender.title = self.config["pause"]
            self.timer.start()
        else:
            sender.title = self.config["continue"]
            self.timer.stop()

    def stop_timer(self):
        self.set_up_menu()
        self.start_pause_button.title = self.config["start"]
    
    def run(self):
        self.app.run()

if __name__ == "__main__":

    appBlocker = AppBlocker()
    appBlocker.run()
