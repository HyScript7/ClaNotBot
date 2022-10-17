FROM python
WORKDIR /
COPY . .

# Install dependencies
RUN ["python", "-m", "pip", "install", "-r", "./requirements.txt"]

# Create Env
ENV TOKEN=""
ENV BAKAUSER=""
ENV BAKAPASS=""

# Run application
CMD ["python3", "./main.py"]

