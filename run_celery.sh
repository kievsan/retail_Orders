celery -A retail_orders -b "redis://127.0.0.1:6379/1" --result-backend "redis://127.0.0.1:6379/2" worker -c 10 -l info --pool=threads
