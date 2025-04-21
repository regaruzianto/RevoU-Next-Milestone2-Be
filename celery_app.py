# from celery import Celery
# import os

# def make_celery(app_name = __name__):
#     return Celery(
#         app_name, 
#         broker=os.getenv('CELERY_BROKER_URL'),
#         backend=os.getenv('CELERY_BROKER_URL')
#     )

# celery = make_celery()