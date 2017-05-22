import machine
import neopixel
import time
from time import sleep

pixel = neopixel.NeoPixel(machine.Pin(15), 12)


def color(ids, colors = (0, 0, 0)):
  if ids == 'off' or 'all':
    for index in range(0, 12):
      pixel[index] = colors

  else:
    for index in range(0, len(ids)):
      pixel[ids[index]] = colors

  pixel.write()

def startup():
  color((3, 9), (22, 224, 59))
  sleep(0.10)
  color('off')
  sleep(0.10)

startup()
