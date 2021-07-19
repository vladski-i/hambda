FROM python:3-slim
ADD . /app
run python3 -m pip install Flask
WORKDIR /app

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]