## install package

$ pip3 install -r requirements.txt


## heroku guide

$ heroku git:remote -a {HEROKU_APP_NAME}

$ heroku login

$ heroku logs --tail

$ heroku ps:scale web=1 worker=1

$ heroku ps


## GCP app engine guide

python3 -m venv env
source env/bin/activate

cd YOUR_PROJECT
pip install  -r requirements.txt

gcloud app create

gcloud app deploy app.yaml \
    --project scrapy-pchome