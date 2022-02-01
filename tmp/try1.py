import pyaudio
import threading
import time
import argparse
import wave
import sys
import numpy as np
from threading import Event

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
                        start = False
                        frames_per_buffer=self.chunk)

    def listen(self, queue):
        while self.stream.is_active():
            data = self.stream.read(self.chunk , exception_on_overflow=False)
            queue.append(data)

    def start_listening(self, queue):
        self.stream.start_stream()
        thread = threading.Thread(target=self.listen, args=(queue,), daemon=True)
        thread.start()
        print("\n listening... \n")

    def stop_listening(self):
        time.sleep(0.01)
        self.stream.stop_stream()



class OnlineSession:

    def __init__(self):
        self.listener = Listener(sample_rate=8000)
        self.audio_q = list()
        self.start = False

    def save(self, waveforms, fname="audio_temp"):
        wf = wave.open(fname, "wb")
        # set the channels
        wf.setnchannels(1)
        # set the sample format
        wf.setsampwidth(self.listener.p.get_sample_size(pyaudio.paInt16))
        # set the sample rate
        wf.setframerate(8000)
        # write the frames as bytes
        wf.writeframes(b"".join(waveforms))
        # close the file
        wf.close()
        return fname

    def inference_loop(self):
        cnt = 0
        print(self.audio_q)
        while True:
            if len(self.audio_q) < 5:
                continue
            else:
                pred_q = self.audio_q.copy()
                self.audio_q.clear()
                print(pred_q, '\n\n')
            cnt+=1
            time.sleep(0.05)

    def run(self):
        self.listener.run(self.audio_q)
        thread = threading.Thread(target=self.inference_loop,
                                    args=(), daemon=True)
        thread.start()

if __name__ == "__main__":

    audio_stream = OnlineSession()
    audio_stream.run()
    print('End')