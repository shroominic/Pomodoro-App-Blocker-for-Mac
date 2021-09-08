from AppKit import NSWorkspace
import subprocess
import appscript
import rumps
import json


def close_app(app):
    print(f'Closing: {app}')
    subprocess.call(['osascript', '-e', f'tell application "{app}" to quit'])


def close_tab(tab, browser='Safari'):
    print(f'Closing: {tab}')
    subprocess.call(['osascript', '-e', f'set closeTab to \"{tab}\" as string',
                     '-e', f'tell application \"{browser}\"',
                     '-e', 'set _W to a reference to every window',
                     '-e', 'repeat with W in _W',
                     '-e', 'close (every tab of W where the name contains closeTab)',
                     '-e', 'end repeat',
                     '-e', 'end tell'])


class AppBlocker(object):
    def __init__(self):
        self.config = None
        self.read_config()

        self.app = rumps.App(self.config["app_name"], "🍅")
        self.timer = rumps.Timer(self.on_tick, 1)
        self.interval = self.config["interval"]
        self.running_apps = []
        self.active_safari_tabs = []

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
        with open('config.json') as config:
            self.config = json.load(config)
            print('Config updated')

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
                    close_app(app)
            elif self.whitelistActiv:
                if app not in self.whitelist:
                    close_app(app)

        if 'Safari' in self.running_apps and 'Safari' not in self.blacklist:
            self.active_safari_tabs = appscript.app('Safari').windows.tabs.URL()[0]
            for tab in self.active_safari_tabs:
                for blocked_site in self.blockedSites:
                    if blocked_site in tab:
                        close_tab(blocked_site)

        if mins == 0 and time_left < 0:
            rumps.notification(title=self.config["app_name"], subtitle=self.config["break_message"], message='')
            self.stop_timer()
        else:
            self.app.title = '{:2d}:{:02d}'.format(mins, secs)

        sender.count += 1

    def start_timer(self, sender):
        self.read_config()
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
