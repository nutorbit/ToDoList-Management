git add .

git commit -m "update"

git push heroku master

heroku config:set WEB_CONCURRENCY=1