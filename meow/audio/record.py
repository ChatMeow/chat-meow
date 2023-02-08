'''
Author: MeowKJ
Date: 2023-01-25 14:25:18
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-08 16:59:36
FilePath: /chat-meow/meow/audio/record.py
'''
import audioop
import pyaudio
import logging
from meow.utils.context import get_record_stop
from meow.utils.context import get_chat_thread_stop_flag
from meow.utils.context import ThreadStopException
import wave
import time
# global audio_frames


class RecordHandler(object):

    stream_format = pyaudio.paInt16
    pyaudio_instance = pyaudio.PyAudio()
 #   sample_width = pyaudio_instance.get_sample_size(stream_format)

    def __init__(self, audio_min_rms=2000, max_low_audio_flag=10, max_high_audio_flag=3, channel=1, rate=44100, chunk=1024):
        # self.source_file = source_file
        self.channels = channel
        self.rate = rate
        self.chunk = chunk
        self.audio_min_rms = audio_min_rms
        self.max_low_audio_flag = max_low_audio_flag
        self.max_high_audio_flag = max_high_audio_flag
        self.audio_frames = []

    def detect_audio(self):
        stream = self.pyaudio_instance.open(format=self.stream_format,
                                            channels=self.channels,
                                            rate=self.rate,
                                            input=True,
                                            frames_per_buffer=self.chunk)
        low_audio_flag = 0
        high_audio_flag = 0
        detect_count = 0
        logging.debug("* start detecting audio ~")

        while True:
            if (get_record_stop()):
                logging.info('STOP THE RECORDING because stop.audio is True')
                stream.close()
                return 1, 'stop'
            if (get_chat_thread_stop_flag()):
                logging.info('STOP THE THREAD because ThreadStopException')
                raise (ThreadStopException)
            
            detect_count += 1

            stream_data = stream.read(self.chunk)

            rms = audioop.rms(stream_data, 2)
            if(detect_count < 10):
                continue

            logging.debug('RECORD  ' + str(rms))
            if rms > self.audio_min_rms:
                high_audio_flag = high_audio_flag + 1
                low_audio_flag = 0
                self.audio_frames.append(stream_data)

            else:
                low_audio_flag = low_audio_flag + 1

            if (detect_count > 10000):
                low_audio_flag = 0
                high_audio_flag = 0
                detect_count = 0
                detect_count = 0

            if low_audio_flag > self.max_low_audio_flag and high_audio_flag > self.max_high_audio_flag:

                logging.debug("* no audio detected, stop detecting ~")
                break
        stream.stop_stream()
        stream.close()
        txt = b''.join(self.audio_frames)
        self.audio_frames = []
        return 0, txt

    def terminate(self):
        self.pyaudio_instance.terminate()


    def play_from_str(self, audio_txt: str) -> None:

        stream = self.pyaudio_instance.open(format=8, channels=1,
                        rate=16000, output=True)
        time.sleep(0.5)
        stream.write(audio_txt)
        stream.stop_stream()
        stream.close()


    def play_from_wav(self, audio_wav: str) -> None:
        chunk = 1024
        f = wave.open(audio_wav, "rb")
        stream = self.pyaudio_instance.open(format=self.pyaudio_instance.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        data = f.readframes(chunk)
        while data != '':
            stream.write(data)
            data = f.readframes(chunk)
        stream.stop_stream()
        stream.close()
