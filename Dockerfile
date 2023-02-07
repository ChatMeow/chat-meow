
FROM python:3
ADD ./ /code
WORKDIR /code
ENV LANG C.UTF-8
EXPOSE 5000 
RUN pip install -r requirements.txt
CMD ["python", "/main.py"]
