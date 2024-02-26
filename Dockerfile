# Use an official Python runtime as a parent image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# 
COPY ./myapp /code/myapp

# 
CMD ["uvicorn", "myapp.main:app", "--host", "0.0.0.0", "--port", "8080"]