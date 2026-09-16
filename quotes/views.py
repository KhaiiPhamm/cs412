from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.

import random

quotes = [
    "“It always seems impossible until it's done.”",
    "“There is nothing like returning to a place that remains unchanged to find the ways in which you yourself have altered.”",
    "“Lead from the back — and let others believe they are in front.”",
    "“There is no passion to be found playing small - in settling for a life that is less than the one you are capable of living.”",
    "“ As we let our own light shine, we unconsciously give other people permission to do the same.”",
    "“May your choices reflect your hopes, not your fears.”",
    "“Appearances matter — and remember to smile.”",
    "“I learned that courage was not the absence of fear, but the triumph over it. The brave man is not he who does not feel afraid, but he who conquers that fear.”"
]

images = [
    "https://cdn.britannica.com/67/75567-050-4EBBE84D/Nelson-Mandela.jpg",
    "https://i0.wp.com/karsh.org/wp-content/uploads/2017/06/Yousuf-Karsh-Nelson-Mandela-1990.jpg?fit=960%2C1235&strip=none&ssl=1",
    "https://myhero.com/content/images/thumbs/0029171_nelson-mandela.jpeg",
    "https://i.natgeofe.com/n/6784d56f-a792-4d57-9a05-f6a9500dd2f2/68382.jpg",
    "https://people.com/thmb/AhO3-d9YLm7x9a0G70QZLo8Zb3U=/4000x0/filters:no_upscale():max_bytes(150000):strip_icc():focal(216x0:218x2)/nelson-mandela-14-435-031cb67cb8a5449ba82bbb4b204a540d.jpg",
    "https://hips.hearstapps.com/hmg-prod/images/_photo-by-per-anders-petterssongetty-images.jpg",
    "https://images-prod.anothermag.com/640/azure/another-prod/270/3/273941.jpg",
    "https://www.psephizo.com/wp-content/uploads/2013/12/nelson-mandela.jpg"
]

def quote(request):
    '''Define a view to show the 'quote.html' template.'''
    
    # the template to which we will delegate the work
    template = 'quote.html'
 
    # a dict of key/value pairs, to be available for use in template
    context = {
        'quote': random.choice(quotes),
        'image': random.choice(images)
    }
 
    return render(request, template, context)

def show_all(request):
    '''Define a view to show the 'show_all.html' template.'''
    
    # the template to which we will delegate the work
    template = 'show_all.html'
 
    # a dict of key/value pairs, to be available for use in template
    context = {
        'quotes': quotes,
        'images': images
    }
 
    return render(request, template, context)

def about(request):
    '''Define a view to show the 'about.html' template.'''
    
    # the template to which we will delegate the work
    template = 'about.html'

    return render(request, template)