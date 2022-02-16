from django.shortcuts import render
import datetime

def home(request):
    date = datetime.datetime.now().date()
    name = 'User1'
    _context = {
        'date': date,
        'name': name
    }
    return render(request, 'index.html', _context)
