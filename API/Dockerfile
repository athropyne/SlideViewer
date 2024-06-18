FROM python:3.12
RUN apt update -y
RUN apt upgrade -y
RUN apt install openslide-tools -y
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]