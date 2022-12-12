#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Pomodoro Focus Timer
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🍅
# @raycast.argument1 { "type": "text", "placeholder": "Interval" }

# Documentation:
# @raycast.description choose your duration in minutes and enjoy distraction free workings
# @raycast.author Shroominic
# @raycast.authorURL https://github.com/Shroominic


import appblocker_mac as appbl
import sys

appBlocker = appbl.AppBlocker()
appBlocker.change_interval(int(sys.argv[1]) * 60)

appBlocker.run()


