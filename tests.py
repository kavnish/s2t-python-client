from onlineSession import onlineSession
from Listener import Listener

from grpc_utils import reqFileTranscript, getTextFromSRT, reqPunctuation
import time

def testOffline(stub, file_path = None):
    file_path = 'demo.wav' if file_path is None else file_path
    print(f'\nInput File - {file_path}\n')
    srt_request = reqFileTranscript(file_path)
    res = stub.recognize_srt(srt_request)
    text = getTextFromSRT(res.srt)
    print(text)
    return
    
def testPunctuation(stub, text = None):
    text = 'hey hi whats up i can give you twenty five' if text is None else text
    hi_text = "इस श्रेणी में केवल निम्नलिखित उपश्रेणी है" # "मेहुल को भारत को सौंप दिया जाए"
    print(f'\nInput Text {text}\n')
    punct_req = reqPunctuation(text, 'en-IN')
    punct_req_hi = reqPunctuation(hi_text, 'hi')
    res = stub.punctuate(punct_req)
    punct_text = res.text
    print(f'\nOutput Text {punct_text}\n')
    return

def testAudioIterator():
    session = onlineSession()
    cache = []
    session.startTest(cache)
    time.sleep(10)
    session.stopTranscription()
    Listener.save('./wavs/alt_buff.wav', session.buffer_chunk)
    return

def testOnline(stub):
    session = onlineSession()
    session.startTranscription(stub)
    print('Press Enter to stop .....')
    input()
    session.stopTranscription()
    Listener.save('./wavs/alt_buff.wav', session.buffer_chunk)
    return
