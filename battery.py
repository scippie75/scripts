#!/usr/bin/python

import time
import subprocess

dim_level = 20
warning_level = 15
shutdown_level = 10

try:
  dimmed = False
  nagged = False
  while True:
    try:
      with open('/sys/class/power_supply/BAT0/status') as f:
        batt_status = f.readline().strip()
      with open('/sys/class/power_supply/BAT0/capacity') as f:
        batt_level = int(f.readline().strip())
      print(f'Battery level: {batt_level} [{batt_status}]')

      if 'Discharging' in batt_status:
        if batt_level <= dim_level and not dimmed:
          subprocess.Popen(['/home/dirk/bin/brightness.py', '0.3'])
          dimmed = True
        if batt_level <= warning_level and not nagged:
          subprocess.Popen(['i3-nagbar', '-m', 'Battery critical! Shutdown now?', '-B', 'Shutdown now!', '"/usr/bin/shutdown -h now"'])
          nagged = True
        if batt_level <= shutdown_level:
          subprocess.Popen(['/usr/bin/shutdown', '-h', 'now'])
      else:
        dimmed = False
        nagged = False
    except ValueError:
      subprocess.Popen(['i3-nagbar', '-m', 'Unable to query battery level'])
    time.sleep(30)
except Exception as e:
  subprocess.Popen(['i3-nagbar', '-m', f'Battery.py script error: {e}'])

