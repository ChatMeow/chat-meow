FROM python:3
WORKDIR /chat
ENV LANG C.UTF-8
EXPOSE 5000
RUN apt-get update -y
RUN apt-get install -y python3-dev portaudio19-dev python3-pyaudio
RUN pip install Flask==2.2.2\
                openai==0.26.2\
                PyAudio==0.2.13\
                PyYAML==6.0\
                requests==2.28.2
CMD ["python", "main.py"]
