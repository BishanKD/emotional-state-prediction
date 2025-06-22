# Dockerfile

# Base image with Python
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --verbose

# NLTK downloads
# RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
RUN python -m nltk.downloader punkt stopwords punkt_tab

# Expose ports
EXPOSE 8000 8501

# Start both FastAPI and Streamlit via shell script
CMD ["bash", "start.sh"]
