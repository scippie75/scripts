#!/usr/bin/python

# Font used for icons is [icofont](https://www.icofont.com)

import os, psutil, time, json
from datetime import datetime

def get_free_space(path):
  st = os.statvfs(path)
  return st.f_bavail * st.f_frsize / 1024 / 1024 / 1024

def get_available_memory():
  vm = psutil.virtual_memory()
  return vm.available / 1024 / 1024 / 1024

def get_battery_status():
  with open('/sys/class/power_supply/BAT0/status') as f:
    batt_status = f.readline().strip()
  with open('/sys/class/power_supply/BAT0/capacity') as f:
    batt_level = int(f.readline().strip())
  return (batt_status, batt_level)

def get_wifi_signal():
  with open('/proc/net/wireless') as f:
    f.readline()
    f.readline()
    code = f.readline()
  status = [ token for token in code.split(' ') if token ]
  if len(status) > 2:
    return 100.0 * float(status[2]) / float(70.0)
  else:
    return None

def get_brightness():
  with open('/home/dirk/.brightness') as f:
    val = f.readline()
  return float(val) * 100

batt_status_icon = {
  'Charging': '',
  'Discharging': '',
  'Full': '',
  'Unknown': '',
}

def ji(name, instance, icon, text, green=None, yellow=None, red=None, gray=None):
  color = 'white'
  if green:
    color = 'green'
  if yellow:
    color = 'yellow'
  if red:
    color = 'red'
  if gray:
    color = 'gray'
  txt = f'<span foreground="#aaa">{icon}</span>  <span foreground="{color}">{text}</span>'
  return { "name": name, "instance": instance, "full_text": txt, "separator": True, "separator_block_width": 54, "markup": "pango" }

if __name__ == '__main__':

  print('{ "version": 1, "stop_signal": 10, "cont_signal": 12, "click_events": true }')
  print('[')
  while True:
    brightness = get_brightness()
    cpu_percent = psutil.cpu_percent()
    available_memory = get_available_memory()
    free_space_root = get_free_space('/')
    free_space_data = get_free_space('/data')
    wifi_signal = get_wifi_signal()
    wifi_signal_status = '{:.0f}%'.format(wifi_signal) if wifi_signal else 'down'
    batt = get_battery_status()
    batt_icon = batt_status_icon[batt[0]] if batt[0] in batt_status_icon else batt_status_icon['Unknown']
    clock = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    j = [
      ji('brightness', 'percent', '', '{:.0f}%'.format(brightness)),
      ji('cpu', 'percent', '', '{:.1f}%'.format(cpu_percent), green=cpu_percent > 10, yellow=cpu_percent > 30, red=cpu_percent > 85),
      ji('memory', 'available', '', '{:.1f}GiB'.format(available_memory), green=available_memory < 25, yellow=available_memory < 10, red = available_memory < 2),
      ji('disk', 'root', ' /', '{:.1f}GiB'.format(free_space_root), green=free_space_root < 100, yellow=free_space_root < 30, red=free_space_root < 2),
      ji('disk', 'data', ' /data', '{:.1f}GiB'.format(free_space_data), green=free_space_data < 100, yellow=free_space_data < 30, red=free_space_data < 2),
      ji('wifi', 'signal', '', wifi_signal_status, green=wifi_signal and wifi_signal < 70, yellow=wifi_signal and wifi_signal < 50, red=wifi_signal and wifi_signal < 30, gray=not wifi_signal),
      ji('battery', 'charge', batt_icon, f'{batt[1]}%', green=batt[0] != 'Full', yellow=batt[1] < 50, red=batt[1] < 20),
      ji('clock', 'current', '', clock)
    ]

    print(json.dumps(j) + ",", flush=True)

    time.sleep(1)

