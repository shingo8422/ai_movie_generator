FROM python:3.11

RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    fonts-freefont-ttf

COPY image_magick_policy.xml /etc/ImageMagick-6/policy.xml

WORKDIR /app

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY poetry.lock /app/
COPY pyproject.toml /app/

RUN poetry install

COPY . /app/

CMD ["python", "main.py"]
