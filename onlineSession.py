
from Listener import Listener
from utils import getRandomUserID
import webrtcvad
import time
import threading
import json

from grpc_utils import Message

class onlineSession:

    def __init__(self, rate = 16000):
        self.stream = Listener(rate = rate, chunk = 1024)
        self.transcript = ''
        self.buffer = []
        self.buffer_chunk = []
        self.user_id = getRandomUserID(7)
        self.sentIdx = 0
        self.lang = 'en-IN'
        #self.vad = webrtcvad.Vad(2)
        self.rate = rate
        self.last_n_frames = []



    def isSpeaking(self, frames, n = 1):
        last_n_frames = self.last_n_frames
        frame_mean = sum(sorted([frame for frame in frames])[:int(0.25 * len(frames))])/len(frames)
        if len(last_n_frames) == n:
            last_n_frames.pop()
            last_n_frames.append(frame_mean)
            speaking = True if sum(last_n_frames)/n > 0 else False

        else:
            last_n_frames.append(frame_mean)
            speaking = True
        return speaking


    def audioIterator(self):
        self.stream.start_listening(self.buffer)
        time.sleep(0.3)
        done = False
        while not done:
            time.sleep(0.3)
            frames = b''.join(self.buffer[self.sentIdx:])
            self.sentIdx = len(self.buffer)
            
            if self.stream.stream.is_active() == False and len(frames) == 0: done = True 

            speaking = self.isSpeaking(frames)

            if speaking:
                self.buffer_chunk.append(frames)
                sendOnce = True

            message = {
                    'audio':frames,
                    'user':self.user_id,
                    'language':self.lang,
                    'speaking':speaking,
                    'isEnd':False if not done else True
                }

            message = Message(**message)
            if sendOnce or speaking:
                if not speaking: sendOnce = False
                yield message 


    def testIterator(self, cache):
        for m in self.audioIterator():
            print(len(m.audio))
            cache.append(m)
        return

    def startTest(self, cache):
        thread = threading.Thread(target=self.testIterator, args=(cache,), daemon=True, name = 'test request iterator')
        thread.start()   
        return

    def requestIterator(self, stub):
        responses = stub.recognize_audio(self.audioIterator())
        for response in responses:          
            transcript = json.loads(response.transcription)
            if 'transcription' in transcript:
                 self.transcript = transcript['transcription']
                 print(self.transcript, end = '\r')

    def startTranscription(self, stub):
        thread = threading.Thread(target=self.requestIterator, args=(stub,), daemon=True, name = 'grpc request iterator')
        thread.start()         
        return 

    def stopTranscription(self, filename = None):
        filename = './wavs/' + str(time.time()) + self.user_id + '.wav' if filename is None else filename
        self.stream.stop_listening()         
        self.stream.save(filename, self.buffer)
        return 
