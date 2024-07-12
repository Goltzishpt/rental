#!/bin/bash

python3.11 -m venv venv
echo 'Virtual environment is ready!'

source venv/bin/activate
if [ $? -eq 0 ]; then
    echo 'Virtual environment activated!'
else
    echo 'Failed to activate virtual environment!'
    exit 1
fi

pip install -r requirements.txt
echo 'Requirements installed!'

export $(grep -v '^#' .env | xargs)

cd rental_scraper
scrapy crawl rental
