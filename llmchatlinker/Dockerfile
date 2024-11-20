FROM python:3.8-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Command to run the FastAPI app with uvicorn
CMD ["python", "-m", "llmchatlinker.main"]