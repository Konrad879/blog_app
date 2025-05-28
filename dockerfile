FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the files
COPY . /app
COPY wait-for-it.sh /wait-for-it.sh


# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Run Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
