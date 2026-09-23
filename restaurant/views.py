"""
    File: views.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 9/23/2026
    Description: View functions for the restaurant app. Handles the main landing page,
    the order page (with a randomized daily special), and the confirmation page, which
    processes the submitted order form and computes the total price.
"""
from django.shortcuts import render
import random
import time
from decimal import Decimal
# Create your views here.

daily_specials = [
    "Extra Protein for FREE",
    "Bonus Spring Roll, IKR?!",
    "FREE Chocolate Smoothie on us",
    "Extra spicyy sauce",
]

def main(request):
    '''Define a view to handle the 'main' request'''
    
	# the template to which we will delegate the work
    template = "restaurant/main.html"
    
    return render(request, template)

def order(request):
    '''Define a view to handle the 'order' request'''

	# the template to which we will delegate the work
    template = "restaurant/order.html"

    # a dict of key/value pairs, to be available for use in template
    context = { 
        'daily_special': random.choice(daily_specials)
    }
    return render(request, template, context)

def confirmation(request):
    '''Define a view to handle the 'confirmation' request'''

	# the template to which we will delegate the work
    template = "restaurant/confirmation.html"
    
    # handle the submitted order form data
    if request.POST:
 
        item1 = request.POST.get('item1')
        item2 = request.POST.get('item2')
        item3 = request.POST.get('item3')
        item4 = request.POST.get('item4')
        item4_size = request.POST.get('item4_size')
        daily_special = request.POST.get('daily_special')
        instructions = request.POST.get('instructions')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        # intializing total, adding up price of items
        total = Decimal('0')
        if item1 is not None: total += Decimal('10.90')
        if item2 is not None: total += Decimal('12.50')
        if item3 is not None: total += Decimal('13.00')
        if item4 is not None: 
            total += Decimal('10.20')
            if item4_size == 'large':
                total += Decimal('2.0')
        # a dict of key/value pairs, to be available for use in template
        context = {
            'item1': item1,
            'item2': item2,
            'item3': item3,
            'item4': item4,
            'item4_size': item4_size,
            'daily_special':  daily_special,
            'instructions': instructions,
            'time': time.ctime(),
            'total': total,
            'name': name,
            'phone': phone,
            'email': email,
        }
        
    return render(request, template, context)
    
    