FROM tiangolo/uwsgi-nginx-flask:python3.6
COPY . /app
RUN python setup.py install
RUN pip3 install uwsgi
RUN uwsgi --socket 127.0.0.1:5000 --wsgi-file main.py --master --processes 4 --threads 2 --callable app