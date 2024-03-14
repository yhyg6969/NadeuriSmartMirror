from django.shortcuts import render
from django.contrib import messages
from .models import Student, InBodyRecord

def inbody(request):
    uid = request.session.get('uid', None)
    print("UID:", uid)

    if not uid:
        messages.error(request, 'User information not found. Please log in.')
        return render(request, 'inbody.html', {'student_data': None, 'most_recent_record': None, 'difference': None})

    student_data = Student.objects.filter(uid=str(uid)).values().first()
    print("Student Data:", student_data)

    if student_data is None:
        messages.error(request, 'Student information not found.')
        return render(request, 'inbody.html', {'student_data': None, 'most_recent_record': None, 'difference': None})

    most_recent_record = InBodyRecord.objects.filter(uid=str(uid)).order_by('-timestamp').first()
    second_recent_record = InBodyRecord.objects.filter(uid=str(uid)).order_by('-timestamp').exclude(record_id=most_recent_record.record_id).first()

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

    context = {
        'student_data': student_data,
        'most_recent_record': most_recent_record,
        'difference': difference,
    }

    if most_recent_record is None or difference is None:
        messages.info(request, '측정된 기록이 없습니다.')

    print("Messages:", messages.get_messages(request))
    return render(request, 'inbody.html', context)
