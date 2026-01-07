# 1️⃣ Use a lightweight Python base image
FROM python:3.10-slim

# 2️⃣ Install system dependencies for OpenCV and YOLO
# These are required for cv2 and other vision processing tasks
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# 3️⃣ Set the working directory inside the container
WORKDIR /app

# 4️⃣ Copy requirements and install Python dependencies
# We do this before copying the code to leverage Docker's layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy all your project folders into the container
# This includes your agents, vision logic, models, and FAISS database
COPY . .

# 6️⃣ Expose the port Hugging Face Spaces expects (7860)
EXPOSE 7860

# 7️⃣ Start the FastAPI server
# We use 'api.main:app' because your main.py is inside the 'api/' folder
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]