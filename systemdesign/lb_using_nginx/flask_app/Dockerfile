FROM python:slim

# Expose the port to internal docker framework
EXPOSE 5000

WORKDIR /flask_app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD python app.py
