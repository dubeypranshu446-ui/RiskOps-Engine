FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /code

# 3. Copy only the requirements first to cache the installations
COPY requirements.txt .

# 4. Install the exact dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your project files (app, artifacts, etc.)
COPY . .

# 6. Expose the port FastAPI uses
EXPOSE 8000

# 7. Start the server when the container boots
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]