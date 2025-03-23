# Use an official Python image as a base
FROM python:3.11.11

# Create non-root user
RUN useradd -m user

# Set the working directory in the container
WORKDIR /home/user/app

# Copy files with correct ownership 
COPY --chown=user:user requirements.txt .
COPY --chown=user:user app.py .
COPY --chown=user:user utils.py .
COPY --chown=user:user src/ src/
COPY --chown=user:user news_articles/ news_articles/
COPY --chown=user:user audio_files/ audio_files/

# Switch to non-root user
USER user

# Set environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Install required dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Expose port 7860 for Hugging Face Spaces
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"]