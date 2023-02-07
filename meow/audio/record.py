'''
Author: MeowKJ
Date: 2023-01-25 14:25:18
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-07 17:53:11
FilePath: /chat-meow/meow/audio/record.py
'''
import audioop
import pyaudio
import logging
from meow.utils.context import get_record_stop

# global audio_frames


class RecordHandler(object):

    stream_format = pyaudio.paInt16
    pyaudio_instance = pyaudio.PyAudio()
 #   sample_width = pyaudio_instance.get_sample_size(stream_format)

    def __init__(self, audio_min_rms=2000, max_low_audio_flag=10, max_high_audio_flag=3, channel=1, rate=16000, chunk=1024):
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
                return 1, 'stop'
            detect_count += 1

            stream_data = stream.read(self.chunk)

            rms = audioop.rms(stream_data, 2)
            if rms > self.audio_min_rms:
                high_audio_flag = high_audio_flag + 1
                low_audio_flag = 0
                self.audio_frames.append(stream_data)

            else:
                low_audio_flag = low_audio_flag + 1
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
