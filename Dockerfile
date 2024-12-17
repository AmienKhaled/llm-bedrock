FROM public.ecr.aws/lambda/python:3.11


COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt -t "${LAMBDA_TASK_ROOT}"


COPY ./tests/ ${LAMBDA_TASK_ROOT}
COPY ./main.py ${LAMBDA_TASK_ROOT}

# Set environment variables
ENV PYTHONPATH=/app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD [ "main.handler" ]