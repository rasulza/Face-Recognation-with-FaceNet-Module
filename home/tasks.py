from celery import shared_task
from datetime import datetime, timedelta, timezone, time
import pytz
from home.models import Order, One_Bread_Order
from django.db.models import Min
from django.utils import timezone
from django.shortcuts import get_object_or_404

@shared_task
def delivery_list():
    user_waiting_time = Order.objects.values_list('waitingـtime',flat=True)
    for user_time in user_waiting_time:
        
        tz_tehran = pytz.timezone('Asia/Tehran')
        datetime_tehran = datetime.now(tz_tehran)
        date_time_format = time(datetime_tehran.hour, datetime_tehran.minute, datetime_tehran.second)
        print(user_time)
        print(date_time_format)
        user_time_now = datetime.combine(datetime.min, date_time_format) - datetime.combine(datetime.min, user_time)
        total_seconds = user_time_now.total_seconds()
        delta = timedelta(seconds=total_seconds)
        dt=datetime.utcfromtimestamp(delta.total_seconds())
        time_format = dt.time()
        Order.objects.filter(created_at__lt=time_format).delete()






