FROM python

WORKDIR /app
COPY app /app
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]