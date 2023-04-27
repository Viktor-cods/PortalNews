from celery import shared_task
import time



@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

def clear_old():
    old_orders = Order.objects.all().exclude(time_in__gt =
                        datetime.now() - timedelta(minutes = 5))
    old_orders.delete()