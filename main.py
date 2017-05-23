import ssd1306
import ure
import utime
import socket
import machine

i2c = machine.I2C(-1, scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
button = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
buttonValue = button.value()
displayLine1 = ''
displayLine2 = ''
displayLine3 = ''

def setDisplay():
  global displayLine1;
  global displayLine2;
  global displayLine3;

  oled.fill(0)
  oled.text(displayLine1, 0, 0)
  oled.text(displayLine2, 0, 10)
  oled.text(displayLine3, 0, 20)
  oled.show()

def setFace(string):
  global displayLine3;

  displayLine3 = '   ' + string

  setDisplay()

def setEmotion(emotionType):
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

    setColor('off')

  elif emotionType == 'sad':
    colors = (56, 82, 124)

    for index in range(0, 4):
      setColor((1,2), colors)
      sleep(0.5);
      setColor('off')

  elif emotionType == 'angry':
    colors = (255, 0, 0)

    for index in range(0, 10):
      setColor('all', colors)
      sleep(0.3);
      setColor('off')

def buttonListen():
  global buttonValue

  while True:
    if (button.value != buttonValue):
      buttonValue = button.value()

      break

def startServer():
  global displayLine1;
  global displayLine2;
  global buttonValue

  print('startServer()')

  addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

  s = socket.socket()
  s.bind(addr)
  s.listen(1)

  while True:
    print('startServer() loop begin')

    # If the button has been pressed (value changed), we'll stop the server.
    if (button.value() != buttonValue):
      buttonValue = button.value()
      buttonListen()
      break

    # Conection started from client.
    cl, addr = s.accept()
    reqLine = cl.readline();

    reqPartsCompile = ure.compile('\s');
    reqParts = reqPartsCompile.split(reqLine);

    commandPattern = ure.compile('\/');
    commandParts = commandPattern.split(reqParts[1]);

    # Ignore first blank result.
    commandPartsLen = int((len(commandParts) - 1))

    print(reqLine)
    print(reqParts)

    print(commandParts)
    print(commandPartsLen)

    print('Command:' + commandParts[1])

    # Command recieved
    if (commandPartsLen > 0):
      command = str(commandParts[1])

      if ((command == 'emotion') and (commandPartsLen >= 2)):
        cl.send('Starting emotion.');

        emotion = commandParts[2]

        setEmotion(emotion)

      elif ((command == 'display') and (commandPartsLen >= 3)):
        cl.send('Starting display.');

        displayLine1 = commandParts[2]
        displayLine2 = commandParts[3]

        if (commandPartsLen >= 4):
          displayLine3 = commandParts[4]

        setDisplay()

      elif ((command == 'color') and (commandPartsLen >= 2)):
        if (commandPartsLen >= 5):
          colorR = int(commandParts[3])
          colorG = int(commandParts[4])
          colorB = int(commandParts[5])

        if (commandParts[2] == 'off'):
          cl.send('Starting color:off.');

          setColor('off')

        elif ((commandParts[2] == 'on') and (commandPartsLen >= 5)):
          cl.send('Starting color:on.');

          setColor('all', (colorR, colorG, colorB))

        elif ((commandParts[2] == 'blink') and (commandPartsLen >= 8)):
          cl.send('Starting color:blink.');

          timeOn = int(commandParts[6]);
          timeOff = int(commandParts[7]);
          loops = int(commandParts[8]);

          for i in range(0, loops):
            setColor((colorR, colorG, colorB));

            utime.sleep_ms(timeOn);

            setColor('off');

            utime.sleep_ms(timeOff);

        else:
          cl.send('Unknown format, or mismatching parameter amount.');

        cl.close();

def introduction():
  global displayLine1;
  global displayLine2;

  setColor('off')

  displayLine1 = 'Hello!'
  displayLine2 = 'Im Mr Cockroach!'

  setDisplay()
  setEmotion('happy')

  displayLine1 = ''
  displayLine2 = 'How U doin?'

  setDisplay()
  setEmotion('cheeky')

  sleep(2)

  displayLine1 = '? What do you'
  displayLine2 = 'mean no thanks?'

  setDisplay()
  setEmotion('surprised')

  sleep(2)

  displayLine1 = 'Noone says no'
  displayLine2 = 'to Mr Cockroach!'

  setDisplay()
  setEmotion('angry')

def startupMain():
  global displayLine1;
  global displayLine2;

  print('startupMain()')
  #introduction();
  setEmotion('surprised')
  displayLine1 = 'My purpose is'
  displayLine2 = 'to pass butter?'
  setDisplay()

  sleep(3)

  displayLine1 = 'I dont even'
  displayLine2 = 'have arms!'
  setDisplay()

  setEmotion('sad')

  if (ssidExists('Reload')):
    doConnect('Reload', 'reloadmenow')

  elif (ssidExists('LANDownUnder')):
    doConnect('LANDownUnder', 'PASSWORD')

  startServer()

startupMain()
