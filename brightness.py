#!/usr/bin/python
# A brightness control script for OLED displays which do not have a backlight to control with xbacklight. The script will search for the primary screen and control the brightness with xrandr. The value of the brightness is stored in a file.
# The script can be used for several things:
# - run it with +value to up the brightness
# - run it with -value to lower the brightness
# - run it with value to set the brightness
# The resulting brightness value must be between 0.0 and 1.0
# The script returns the current value of the brightness (between 0.0 and 1.0) so you can use the script also without parameter to show the value on a status bar like i3blocks.

import sys
import subprocess

display = subprocess.check_output("xrandr | grep ' connected' | awk '{ print $1 }'", shell=True).decode('utf-8').strip()

brightness = 1.0
try:
  with open('/home/dirk/.brightness', 'r') as f:
    brightness = float(f.read())
except:
  pass

if len(sys.argv) == 2:
  p = sys.argv[1]
  if p[0] == '+':
    brightness = brightness + float(p[1:])
  elif p[0] == '-':
    brightness = brightness - float(p[1:])
  else:
    brightness = float(p)

brightness = max(0.0, min(1.0, brightness))

subprocess.run(['xrandr', '--output', display, '--brightness', str(brightness)])

with open('/home/dirk/.brightness', 'w') as f:
  f.write(str(brightness))

print(brightness)

