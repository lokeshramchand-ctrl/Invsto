FROM python:3.10-slim

WORKDIR /app

# Install system deps
# Added libatomic1: Required for Prisma's internal Node.js engine on slim images
RUN apt-get update && apt-get install -y curl libatomic1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generate Prisma Client
RUN prisma generate

EXPOSE 8500

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]