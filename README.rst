gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

poetry export -f requirements.txt --output requirements.txt --without-hashes

gcloud builds submit --tag gcr.io/zone-india/auth-api-container

gcloud run deploy --image gcr.io/zone-india/auth-api-container --platform managed