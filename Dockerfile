FROM python AS builder
EXPOSE 8000
WORKDIR /backend
COPY . /backend
RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt 
ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]