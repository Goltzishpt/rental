#!/bin/bash
set -xe
VENV="venv"

python3.11 -m venv "${VENV}"

source "${VENV}"/bin/activate

pip install -r requirements.txt

export $(grep -v '^#' .env | xargs)

cd rental_scraper
scrapy crawl rental
