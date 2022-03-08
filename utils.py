import pyaudio
import string
import random
import json


def readWAVFile(path):
        with open(path, 'rb') as f:
            arr = f.read()
        return arr 

def writeJSON(path, data):
    with open(path, 'w') as f:
        json.dumps(data)


def getStream(rate = 16000, chunk = 4096):
      channels = 1
      formt = pyaudio.paInt16 #p.get_format_from_width(2)
      p = pyaudio.PyAudio()
      stream = p.open(format=formt,
                      channels=channels,
                      rate=rate,
                      input=True,
                      start = False,
                      frames_per_buffer=chunk)
      return stream 

def getRandomUserID(n = 7):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k = n))
