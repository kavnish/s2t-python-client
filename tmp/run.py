from client.infer_pb2 import PunctuateRequest
from client.infer_pb2_grpc import RecognizeStub
import grpc
from client.infer_pb2 import PunctuateRequest, Message, PunctuateResponse, SRTRequest, SRTResponse, Response
import pyaudio
import time
import threading



class Listener:

    def __init__(self, sample_rate=8000, record_seconds=2):
        self.chunk = 1024
        self.sample_rate = sample_rate
        self.record_seconds = record_seconds
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=self.chunk)

    def listen(self, queue):
        while True:
            data = self.stream.read(self.chunk , exception_on_overflow=False)
            queue.append(data)
            time.sleep(0.01)

    def run(self, queue):
        thread = threading.Thread(target=self.listen, args=(queue,), daemon=True)
        thread.start()
        print("\Speech Recognition engine is now listening... \n")


def testInferService():   

    channel = grpc.insecure_channel('10.140.102.229:5001')
    stub = RecognizeStub(channel)

    punctuate_request = PunctuateRequest(
        text = 'hi whats up'
        , language = 'en-IN'
        , enabledItn = False
    )
    res = stub.punctuate(punctuate_request, timeout=3)

    print(res.text, sep = '\n\n')

    return 

def main():
    buffer = []
    stream = Listener(8000, 5)
    stream.run(buffer)
    # run(stream, buffer)
    return

def run(stream, buffer):
    thread = threading.Thread(target=stream.run,
                                args=(buffer,), daemon=True)
    thread.start()
    return


if __name__ == "__main__":
    main()



