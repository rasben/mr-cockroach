import machine
import neopixel
import network
import time
from time import sleep

pixel = neopixel.NeoPixel(machine.Pin(15), 12)

def setColor(ids, colors = (0, 0, 0)):
  if ids == 'off' or 'all':
    for index in range(0, 12):
      pixel[index] = colors

  else:
    for index in range(0, len(ids)):
      pixel[ids[index]] = colors

  pixel.write()

def ssidExists(ssid):
  sta_if = network.WLAN(network.STA_IF)

  for networkElement in sta_if.scan():
    if (networkElement[0].decode("utf-8") == ssid):
      return True

  return False

# Define a simple method which connects to your WiFi
def doConnect(ssid, password):
    # Disable the ESP's built-in access point.
    ap = network.WLAN(network.AP_IF)
    if ap.active():
        ap.active(False)

    # Enable the ESP's station mode for connecting as a client.
    wlan = network.WLAN(network.STA_IF)

    wlan.active(True)
    # Check if we are already connected.
    if not wlan.isconnected():
        # Connect with the provided credentials.
        print('Connecting to network...')
        wlan.ifconfig(('192.168.168.123', '255.255.255.0', '192.168.168.1', '8.8.8.8'))
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass

    # Finally, print out the current netconfig.
    print('Network config:', wlan.ifconfig())

def startupBoot():
  setColor((3, 9), (22, 224, 59))
  sleep(0.30)
  setColor('off')

  #if (ssidExists('Reload')):
    #doConnect('Reload', 'reloadmenow')

startupBoot()
