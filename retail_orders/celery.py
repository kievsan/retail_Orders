# переменная окружения DJANGO_SETTINGS_MODULE для командной строки Celery.
import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retail_orders.settings')
django.setup()

from celery import Celery

from celery.result import AsyncResult

# экземпляр приложения
app = Celery('retail_orders',
             backend="redis://localhost:6379/2",
             broker="redis://localhost:6379/1",
             include=[
                 'api.tasks',
             ])

# namespace определяет префикс, который в settings.py будет у настроек, связанных с Celery.
# настройки вида CELERY_, например CELERY_BROKER_URL;
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery будет искать файл tasks.py в каждом каталоге приложений, добавленных в INSTALLED_APPS,
# чтобы загружать определенные в нем "асинхронные" задания.
app.autodiscover_tasks()

def get_task_result(task_id: str) -> AsyncResult:
    print('start def celery_app.get_task')  #############
    return AsyncResult(task_id, app=app)

#
""" ЗАМЕЧАНИЯ:
        Запустить Celery в отдельной вкладке терминала ( разработка, не в контейнере )
        export DJANGO_SETTINGS_MODULE=retail_orders.settings
        celery -A retail_orders worker -E -l info -P threads
    
    Если ОШИБКА про DJANGO_SETTINGS_MODULE:
        1.	редактировать файл окружения	        venv/bin/activate в Linux,  ( venv/Scripts/activate в Windows )
	        добавить в самый конец файла: 			export DJANGO_SETTINGS_MODULE=retail_orders.settings
	        добавить в конец раздела  deactivate:	unset DJANGO_SETTINGS_MODULE
        2.	перезапустить:	 						source venv/bin/activate    ( venv/Scripts/activate.bat в Windows )
        3.	проверить:								echo $DJANGO_SETTINGS_MODULE
        4. 	снова запустить celery    
"""
