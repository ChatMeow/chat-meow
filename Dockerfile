FROM python:3
ADD ./ /code
WORKDIR /code
ENV LANG C.UTF-8
EXPOSE 5000
RUN apt-get update -y
RUN apt-get install -y python3-dev portaudio19-dev python3-pyaudio
RUN pip install -r requirements.txt
CMD ["python", "/main.py"]
