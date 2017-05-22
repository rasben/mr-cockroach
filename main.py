import ssd1306

i2c = machine.I2C(-1, scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
button = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)

def setFace(string):
  oled.show()
  oled.text(string, 30, 20)
  oled.show()

def emotion(emotionType):
  if emotionType == 'happy':
    face = '( ^ . ^ )'
  elif emotionType == 'sad':
    face = '( \' . \' )'
  elif emotionType == 'cheeky':
    face = '( ^ . - )'
  elif emotionType == 'surprised':
    face = '( o _ O )'
  elif emotionType == 'angry':
    face = '( @ _ @ )'

  setFace(face)

  if emotionType == 'happy':
    colors = (235, 66, 244)

    for index in range(0, 11):
      if (index > 0):
        pixel[index - 1] = (0, 0, 0)

      pixel[index] = colors
      pixel.write()

      sleep(0.3)

    color('off')

  elif emotionType == 'sad':
    colors = (235, 66, 244)

    for index in range(0, 2):
      color((1,2), colors)
      sleep(0.5);
      color('off')

  elif emotionType == 'angry':
    colors = (255, 0, 0)

    for index in range(0, 10):
      color('all', colors)
      sleep(0.3);
      color('off')

def mainup():
  color('off')

  oled.text('Hello!', 40, 0)
  oled.text('Im Mr Cockroach!', 0, 10)
  oled.show()
  emotion('happy')

  oled.fill(0)
  oled.show()

  emotion('cheeky')
  oled.text('Send nudes?', 20, 10)
  oled.show()

  sleep(2)
  oled.fill(0)
  oled.show()

  emotion('surprised')
  oled.text('What, no?', 22, 10)
  oled.show()

  sleep(2)

  oled.fill(0)
  oled.show()

  emotion('angry')
  oled.text('Noone says no', 0, 0)
  oled.text('to Mr Cockroach!', 0, 10)
  oled.show()

mainup()