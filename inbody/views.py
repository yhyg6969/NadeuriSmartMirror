from django.shortcuts import render
from django.contrib import messages
from datetime import datetime, timedelta
from .models import Student, GameRecord, InBodyRecord

def inbody(request):
    uid = request.session.get('uid', None)

    if not uid:
        messages.error(request, 'User information not found. Please log in.')
        return render(request, 'inbody.html', {'student_data': None, 'inbody_records': None})

    # Query the database using uid to get user-specific data
    student_data = Student.objects.filter(uid=str(uid)).values().first()

    if student_data is None:
        messages.error(request, 'Student information not found.')
        return render(request, 'inbody.html', {'student_data': None, 'inbody_records': None})

    # Calculate start and end timestamps for today
    today = datetime.now().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    # Fetching inbody records for today's date
    inbody_records = InBodyRecord.objects.filter(
        uid=str(uid), 
        timestamp__range=(start_of_day.timestamp(), end_of_day.timestamp())
    ).exclude(record_id__isnull=True, uid__isnull=True, timestamp__isnull=True).values(
        'height', 'weight', 'fat', 'fat_ratio', 'muscle', 'skeletal_muscle', 'water_content', 'bmi'
    )

    # Pass the data to the template
    context = {
        'student_data': student_data,
        'inbody_records': inbody_records,
    }

    return render(request, 'inbody.html', context)
