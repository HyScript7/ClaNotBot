
# ClaNotBot

## About

A discord bot that wraps iCanteen and Bakaláři using requests and discord.py
Written in python 3 by HyScript7 and Mobilex

You are free to distribute, modify and use the application under the same license.

## Setup

### Running in a shell

```bash
python3 -m pip install -r ./requirements.txt
python3 ./main.py
```

### Using Docker

Create a docker-compose.yml file:

```yml
version: "3.9"
services:
  bot:
    build: .
    restart: always
```

Creating and running:

```bash
docker-compose up -d
```

Stopping and removing:

```bash
docker-compose down
```

## License & Copyright

ClaNotBot is licensed under MIT License
Copyright (c) 2022 HyScript7 & mobilex1122
