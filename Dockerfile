FROM python:3.10.6

ADD rss-ntfy.py .

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./rss-ntfy.py" ]
