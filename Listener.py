import pyaudio
import threading
import time
import wave

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
