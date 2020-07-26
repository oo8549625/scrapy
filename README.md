## install package

$ pip3 install -r requirements.txt


## heroku guide

$ heroku git:remote -a {HEROKU_APP_NAME}

$ heroku login

$ heroku logs --tail

$ heroku ps:scale web=1 worker=1

$ heroku ps


## GCP app engine guide

$ gcloud app regions list

$ gcloud app create --project=pchome-scrapy --region=asia-east2