import pyaudio
import time
import grpc
import wave
from getpass import getpass
import threading
import string
import random
from client.infer_pb2_grpc import RecognizeStub
from client.infer_pb2 import PunctuateRequest, Message, PunctuateResponse, SRTRequest, SRTResponse, Response


#*-*-*         GRPC Client         *-*-*#
def getStub():
    channel = grpc.insecure_channel('10.140.102.229:5001')
    stub = RecognizeStub(channel)
  663      return stub
  664  def readWAVFile(path):
  665      with open(path, 'rb') as f:
  666          arr = f.read()
  667      return arr 
  668  def reqFileTranscript(path):
  669      buffer = readWAVFile(path)
  670      req = {
  671          "audio" : buffer,
  672          "user" : 'asdasdasdasd',
  673          "language" : "en-IN",
  674          "filename" : 'filename.wav'
  675      }
  676      srt_request = SRTRequest(**req)
  677      return srt_request
  678  def getTextFromSRT(srt):
  679      lst_sessions = list(map(lambda x:x.split('\n'), srt.split('\n\n')))
  680      text = '_'.join([item for slst in [x[2:] for x in lst_sessions if len(x)>=3] for item in slst])
  681      return text
  682  def reqPunctuation(text, lang):
  683      req = {
  684          "text" : text,
  685          "language" : lang,
  686          "enabledItn" : False,
  687      }
  688      punct_request = PunctuateRequest(**req)
  689      return punct_request
  690  def getStream(rate = 16000, chunk = 4096):
  691      channels = 1
  692      formt = pyaudio.paInt16 #p.get_format_from_width(2)
  693      p = pyaudio.PyAudio()
  694      stream = p.open(format=formt,
  695                      channels=channels,
  696                      rate=rate,
  697                      input=True,
  698                      start = False,
  699                      frames_per_buffer=chunk)
  700      return stream 
  701  def reqMessage(stream, CHUNK, user, lang):
  702      while stream.is_active():
  703          frames = stream.read(CHUNK, exception_on_overflow = False)
  704          message = {
  705                  'audio':frames,
  706                  'user':user,
  707                  'language':lang,
  708                  'speaking':True
  709              }
  710          message = Message(**message)
  711          yield message
  712  def callTranscript(stub, generator):
  713      responses = stub.recognize_audio(generator)
  714      for response in responses:;         transcript = response.transcription
  715          print(transcript)
  716  def getRandomUserID(n = 7):
  717      return ''.join(random.choices(string.ascii_uppercase + string.digits, k = n))


  718  class Listener:
  719      def __init__(self, rate = 16000, chunk = 4096):
  720          self.rate = rate
  721          self.chunk = chunk
  722          self.channels = 1
  723          self.formt = pyaudio.paInt16 #p.get_format_from_width(2)
  724          self.p = pyaudio.PyAudio()
  725          self.stream = self.p.open(format=self.formt,
  726                          channels=self.channels,
  727                          rate=rate,
  728                          input=True,
  729                          start = False,
  730                          frames_per_buffer=chunk)
  731          self.RECORD = False
  732      def listen(self, queue):
  733          while self.stream.is_active():
  734              data = self.stream.read(self.chunk , exception_on_overflow=False)
  735              queue.append(data)
  736      def start_listening(self, queue):
  737          self.stream.start_stream()         thread = threading.Thread(target=self.listen, args=(queue,), daemon=True, name = 'stream thread')
  738          thread.start()         print("\n listening... \n")
  739      def stop_listening(self):
  740          time.sleep(1)
  741          self.stream.stop_stream()     @staticmethod
  742      def save(filename, buffer):
  743          with wave.open(filename, 'wb') as wf:
  744              wf.setnchannels(1)
  745              wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
  746              wf.setframerate(16000)
  747              wf.writeframes(b''.join(buffer))
  748          return


  749  class onlineSession:
  750      def __init__(self):
  751          self.stream = Listener(rate = 16000, chunk = 1024)
  752          self.transcript = ''
  753          self.buffer = []
  754          self.buffer_chunk = []
  755          self.user_id = getRandomUserID(7)
  756          self.sentIdx = 0
  757      def audioIterator(self):
  758          self.stream.start_listening(self.buffer)
  759          while self.sentIdx != len(self.buffer):
  760              frames = self.buffer[self.sentIdx:]
  761              self.sentIdx = len(self.buffer)
  762              message = {
  763                      'audio':frames,
  764                      'user':self.user_id,
  765                      'language':self.lang,
  766                      'speaking':True,
  767                      'isEnd':False
  768                  }
  769              message = Message(**message)
  770              yield message 
  771      def requestIterator(self, stub):
  772          responses = stub.recognize_audio(self.audioIterator())
  773          for response in responses:;             transcript = response.transcription
  774              self.transcript = transcript
  775              print(transcript)
  776      def startTranscription(self, stub):
  777          thread = threading.Thread(target=self.requestIterator, args=(stub,), daemon=True, name = 'grpc request iterator')
  778          thread.start()         return 
  779      def stopTranscription(self, filename = None):
  780          filename = str(time.time()) + self.user_id + '.wav' if filename is None else filename
  781          self.stream.stop_listening()         self.stream.save(filename, self.buffer)
  782          return 
  783  def testOffline():
  784      stub = getStub()
  785      file_path = 'demo.wav'
  786      srt_request = reqFileTranscript(file_path)
  787      res = stub.recognize_srt(srt_request)
  788      text = getTextFromSRT(res.srt)
  789      print(text)
  790      return
  791  def testPunctuation():
  792      stub = getStub()
  793      text = 'hey hi whats up i can give you twenty five'
  794      hi_text = "इस श्रेणी में केवल निम्नलिखित उपश्रेणी है" # "मेहुल को भारत को सौंप दिया जाए"
  795      punct_req = reqPunctuation(text, 'en-IN')
  796      punct_req_hi = reqPunctuation(hi_text, 'hi')
  797      res = stub.punctuate(punct_req)
  798      punct_text = res.text
  799      print(punct_text)
  800      return
  801  #*-*-*         main         *-*-*#
  802  #stub = getStub()
  803  session = onlineSession()
  804  for m in session.audioIterator():
  805      print(m)
  806  time.sleep(5)
  807  session.stopTranscription()
