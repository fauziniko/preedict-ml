# Gunakan base image resmi Python
FROM python:3.9-slim

# Set working directory di dalam container
WORKDIR /app

# Salin file requirements.txt untuk menginstal dependencies
COPY requirements.txt .

# Install dependencies Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi ke dalam container
COPY . .

# Expose port Flask
EXPOSE 5000

# Set entrypoint untuk menjalankan aplikasi Flask
CMD ["python", "app.py"]
