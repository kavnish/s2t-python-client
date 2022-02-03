
import webrtcvad
import grpc
from client.infer_pb2_grpc import RecognizeStub
from client.infer_pb2 import PunctuateRequest, Message, PunctuateResponse, SRTRequest, SRTResponse, Response

from utils import readWAVFile

def getStub():
      channel = grpc.insecure_channel('10.140.102.229:5001')
      stub = RecognizeStub(channel)
      return stub

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
            "enabledItn" : True,
        }
        punct_request = PunctuateRequest(**req)
        return punct_request

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
        for response in responses:        
            transcript = response.transcription
            print(transcript)


