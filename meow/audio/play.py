import pyaudio

def play(audio_txt: str) -> None:
    p = pyaudio.PyAudio()

    stream = p.open(format=8, channels=1,
                    rate=16000, output=True)

    stream.write(audio_txt)

    stream.stop_stream()
    stream.close()
    p.terminate()
