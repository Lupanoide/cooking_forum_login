FROM python:3.11-slim
ADD requirements.txt /
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
ADD . /cooking_forum_login
ENV PYTHONPATH=$PYTHONPATH:/cooking_forum_login/
WORKDIR /cooking_forum_login/src/app/
EXPOSE 8000
CMD uvicorn --host 0.0.0.0 main:app