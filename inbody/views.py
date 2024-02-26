from django.shortcuts import render
from django.contrib import messages
from datetime import datetime, timedelta
from .models import Student, GameRecord, InBodyRecord

def inbody(request):
    uid = request.session.get('uid', None)

    if not uid:
        messages.error(request, 'User information not found. Please log in.')
        return render(request, 'inbody.html', {'student_data': None, 'most_recent_record': None, 'difference': None})

    # Query the database using uid to get user-specific data
    student_data = Student.objects.filter(uid=str(uid)).values().first()

    if student_data is None:
        messages.error(request, 'Student information not found.')
        return render(request, 'inbody.html', {'student_data': None, 'most_recent_record': None, 'difference': None})

    # Fetch the most recent inbody record for the user
    most_recent_record = InBodyRecord.objects.filter(uid=str(uid)).order_by('-timestamp').first()

    # Fetch the second most recent inbody record for the user
    second_recent_record = InBodyRecord.objects.filter(uid=str(uid)).order_by('-timestamp').exclude(record_id=most_recent_record.record_id).first()

    # Calculate the difference between most recent and second most recent data
    difference = None
    if most_recent_record and second_recent_record:
        difference = {}
        for field in ['height', 'weight', 'fat', 'fat_ratio', 'muscle', 'skeletal_muscle', 'water_content', 'bmi']:
            recent_value = getattr(most_recent_record, field)
            second_recent_value = getattr(second_recent_record, field)
            diff = recent_value - second_recent_value
            if diff > 0:
                difference[field] = f'({diff:.2f} ▲)'
            elif diff < 0:
                difference[field] = f'({abs(diff):.2f} ▼)'
            else:
                difference[field] = '(차이가 없습니다)'
    elif most_recent_record:
        messages.warning(request, 'Only one inbody record found for this student.')

    # Pass the data to the template
    context = {
        'student_data': student_data,
        'most_recent_record': most_recent_record,
        'difference': difference,
    }

    return render(request, 'inbody.html', context)



