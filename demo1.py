import pyaudio
import time
import grpc
import wave
from getpass import getpass
import threading
import string
import random
import json
from client.infer_pb2_grpc import RecognizeStub
from client.infer_pb2 import PunctuateRequest, Message, PunctuateResponse, SRTRequest, SRTResponse, Response


#*-*-*         GRPC Client         *-*-*#
def getStub():
      channel = grpc.insecure_channel('10.140.102.229:5001')
      stub = RecognizeStub(channel)
      return stub

def readWAVFile(path):
        with open(path, 'rb') as f:
            arr = f.read()
        return arr 

def reqFileTranscript(path):
        buffer = readWAVFile(path)
        req = {
            "audio" : buffer,
            "user" : 'asdasdasdasd',
            "language" : "en-IN",
            "filename" : 'filename.wav'
        }
        srt_request = SRTRequest(**req)
        return srt_request

def getTextFromSRT(srt):
        lst_sessions = list(map(lambda x:x.split('\n'), srt.split('\n\n')))
        text = '_'.join([item for slst in [x[2:] for x in lst_sessions if len(x)>=3] for item in slst])
        return text

def reqPunctuation(text, lang):
        req = {
            "text" : text,
            "language" : lang,
            "enabledItn" : False,
        }
        punct_request = PunctuateRequest(**req)
        return punct_request

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

def reqMessage(stream, CHUNK, user, lang):
        while stream.is_active():
            frames = stream.read(CHUNK, exception_on_overflow = False)
            message = {
                    'audio':frames,
                    'user':user,
                    'language':lang,
                    'speaking':True
                }
            message = Message(**message)
            yield message

def callTranscript(stub, generator):
        responses = stub.recognize_audio(generator)
        for response in responses:;         
            transcript = response.transcription
            print(transcript)

def getRandomUserID(n = 7):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k = n))


  class Listener:

        def __init__(self, rate = 16000, chunk = 4096):
            self.rate = rate
            self.chunk = chunk
            self.channels = 1
            self.formt = pyaudio.paInt16 #p.get_format_from_width(2)
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=self.formt,
                            channels=self.channels,
                            rate=rate,
                            input=True,
                            start = False,
                            frames_per_buffer=chunk)
            self.RECORD = False

        def listen(self, queue):
            while self.stream.is_active():
                data = self.stream.read(self.chunk , exception_on_overflow=False)
                queue.append(data)

        def start_listening(self, queue):
            self.stream.start_stream()         
            thread = threading.Thread(target=self.listen, args=(queue,), daemon=True, name = 'stream thread')
            thread.start()
            print("\n listening... \n")
            return 

        def stop_listening(self):
            time.sleep(1)
            self.stream.stop_stream()
            print("\n Stopped listening! \n")



        @staticmethod
        def save(filename, buffer):
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(16000)
                wf.writeframes(b''.join(buffer))
            return


class onlineSession:

    def __init__(self):
        self.stream = Listener(rate = 16000, chunk = 1024)
        self.transcript = ''
        self.buffer = []
        self.buffer_chunk = []
        self.user_id = getRandomUserID(7)
        self.sentIdx = 0

    def audioIterator(self):
        self.stream.start_listening(self.buffer)
        time.sleep(0.3)
        done = False
        while not done:
            time.sleep(0.3)
            frames = self.buffer[self.sentIdx:]
            self.sentIdx = len(self.buffer)
            if self.stream.stream.is_active() == False and len(frames) = 0: done = True 
            self.buffer_chunk.append(frames)
            message = {
                    'audio':frames,
                    'user':self.user_id,
                    'language':self.lang,
                    'speaking':True,
                    'isEnd':False if not done else True
                }
            message = Message(**message)
            yield message 

    def testIterator(self, cache):
        for m in audioIterator:
            print(len(m.audio))
            cache.append(m)
        return

    def startTest(self, cache):
        thread = threading.Thread(target=self.testIterator, args=(cache,), daemon=True, name = 'test request iterator')
        thread.start()   
        return

    def requestIterator(self, stub):
        responses = stub.recognize_audio(self.audioIterator())
        for response in responses:;             
            transcript = json.loads(response.transcription)
            if 'transcription' in transcript:
                 self.transcript = transcript['transcription']
                 print(self.transcript)
            print(transcript)

    def startTranscription(self, stub):
        thread = threading.Thread(target=self.requestIterator, args=(stub,), daemon=True, name = 'grpc request iterator')
        thread.start()         
        return 

    def stopTranscription(self, filename = None):
        filename = str(time.time()) + self.user_id + '.wav' if filename is None else filename
        self.stream.stop_listening()         
        self.stream.save(filename, self.buffer)
        return 


def testOffline():
    stub = getStub()
    file_path = 'demo.wav'
    srt_request = reqFileTranscript(file_path)
    res = stub.recognize_srt(srt_request)
    text = getTextFromSRT(res.srt)
    print(text)
    return
    
def testPunctuation():
    stub = getStub()
    text = 'hey hi whats up i can give you twenty five'
    hi_text = "इस श्रेणी में केवल निम्नलिखित उपश्रेणी है" # "मेहुल को भारत को सौंप दिया जाए"
    punct_req = reqPunctuation(text, 'en-IN')
    punct_req_hi = reqPunctuation(hi_text, 'hi')
    res = stub.punctuate(punct_req)
    punct_text = res.text
    print(punct_text)
    return

#*-*-*         main         *-*-*#
#stub = getStub()

session = onlineSession()
cache = []
session.startTest(cache)
time.sleep(5)
session.stopTranscription()