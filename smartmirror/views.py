from django.shortcuts import render
from django.contrib import messages
from django.db.models import Sum, F
from datetime import datetime, timedelta
from django.utils import timezone
from .models import GameRecord, Student

def smartmirror(request):
    uid = request.session.get('uid', None)

    if not uid:
        messages.error(request, 'User information not found. Please log in.')
        return render(request, 'smartmirror.html', {'user_info': None})

    # Query the database using uid to get user-specific data
    student_data = Student.objects.filter(uid=str(uid)).values().first()

    if student_data is None:
        messages.error(request, 'Student information not found.')
        return render(request, 'smartmirror.html', {'user_info': None})

    # Pass the data to the template
    context = {
        'uid': uid,
        'student_data': student_data,
    }

    return render(request, 'smartmirror.html', context)
