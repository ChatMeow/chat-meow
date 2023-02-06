import pyaudio
import wave

def play(audio_txt: str) -> None:
    p = pyaudio.PyAudio()

    stream = p.open(format=8, channels=1,
                    rate=16000, output=True)

    stream.write(audio_txt)

    stream.stop_stream()
    stream.close()
    p.terminate()


def play_wav(audio_wav: str) -> None:
    chunk = 1024
    f = wave.open(audio_wav, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    data = f.readframes(chunk)
    while data != '':
        stream.write(data)
        data = f.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()