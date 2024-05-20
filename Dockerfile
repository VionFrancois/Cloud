FROM python:3.10

WORKDIR /service

# Copy all the necessary files to the container
COPY searchEngine/ /service/searchEngine/

RUN pip install -r /service/searchEngine/requirements.txt

# Opens port 8000
EXPOSE 8000

RUN chmod +x /service/searchEngine/start.sh

CMD ["/service/searchEngine/start.sh"]