#!/bin/bash
cd /service/searchEngine
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80