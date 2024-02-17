FROM ubuntu:24.04
LABEL authors="AetherMagee"
WORKDIR /app
RUN apt update -y -qq && apt upgrade -y -qq
RUN apt install -y -qq python3 python3-pip --no-install-recommends
RUN apt autoclean -y -qq && apt autoremove -y -qq
RUN pip install --upgrade pip --break-system-packages --no-cache-dir
COPY requirements.txt .
RUN pip3 install -r requirements.txt --break-system-packages --no-cache-dir
COPY . .
EXPOSE 25565
CMD ["python3", "main.py"]
