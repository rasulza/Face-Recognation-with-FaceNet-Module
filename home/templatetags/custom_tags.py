from django import template
from home.models import One_Bread_Order, Order
import queue

register = template.Library()

@register.inclusion_tag('home/object_list.html')
def queue_list():
    numbers = Order.objects.all()
    ones = One_Bread_Order.objects.all()
    numbers_queue = queue.Queue()
    ones_queue = queue.Queue()

    for num in numbers:
        numbers_queue.put(num, num.waitingـtime)

    for one in ones:
        ones_queue.put(one,one.waitingـtime)

    nums_and_ones = queue.Queue()
    while True:
        if not numbers_queue.empty():
            nums_and_ones.put(numbers_queue.get())
        if not ones_queue.empty():
            nums_and_ones.put(ones_queue.get())
        
        if  numbers_queue.empty() and ones_queue.empty():
            break
    nums_and_ones_list = list(nums_and_ones.queue)
    print(nums_and_ones_list)

    return {'nums_and_ones':nums_and_ones_list}











