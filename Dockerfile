FROM python:3.10-bullseye

WORKDIR /app

# Step 1: Update + Install all necessary system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libgthread-2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    wget \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Step 2: Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 3: Add source code
COPY . .

# Step 4: Expose port for Render to auto-detect
EXPOSE 10000

# Step 5: Run FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]

