FROM python:3.10
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]
