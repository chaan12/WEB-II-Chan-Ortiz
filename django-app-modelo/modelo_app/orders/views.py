from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

def index(request):  
    questions = Question.objects.all()
    data = {
        "questions": questions,
        "titulo": "Index de Orders por variable",
        "total_orders": 100,
        "total_payments": 200,
        "orders": [
            {"id": 1, "total": 100},
            {"id": 2, "total": 200},
            {"id": 3, "total": 300},
            {"id": 4, "total": 400}
        ]
    }
    return render(request, 'orders/index.html', data)
