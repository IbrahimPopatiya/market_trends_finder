FROM python:3.10-slim

WORKDIR /run

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt openai python-dotenv

# Copy code
COPY system/ /app/system/
COPY utils/ /app/utils/

# Run agent
ENTRYPOINT ["python", "/app/system/agent_cli.py"]