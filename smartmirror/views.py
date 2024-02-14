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

    # Calculate today's total activity time and calories
    start_time_today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_time_today = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)

    records_today = GameRecord.objects.filter(
        uid=uid,
        game_type='game3',  # Filter for game3
        start_ts__range=(start_time_today.timestamp(), end_time_today.timestamp())
    )

    total_today_activity_time_seconds = sum(record.finish_ts - record.start_ts for record in records_today)
    total_today_calories = (total_today_activity_time_seconds / 60) * 7

    total_today_activity_time = timedelta(seconds=int(total_today_activity_time_seconds))
    total_today_activity_time_hours, remainder = divmod(total_today_activity_time.seconds, 3600)
    total_today_activity_time_minutes, total_today_activity_time_seconds = divmod(remainder, 60)

    # Query the game records for the specified UID (total activity time and calories)
    start_time = timezone.now() - timedelta(days=365)
    end_time = timezone.now()

    records = GameRecord.objects.filter(
        uid=uid,
        game_type='game3',  # Filter for game3
        start_ts__range=(start_time.timestamp(), end_time.timestamp())
    )

    total_activity_time_seconds = sum(record.finish_ts - record.start_ts for record in records)
    total_calories = (total_activity_time_seconds / 60) * 7

    total_activity_time = timedelta(seconds=int(total_activity_time_seconds))
    total_activity_time_hours, remainder = divmod(total_activity_time.seconds, 3600)
    total_activity_time_minutes, total_activity_time_seconds = divmod(remainder, 60)

    # Print information for debugging
    print("Records Today:", records_today)
    print("All Records:", records)
    print("Total Today Activity Time (seconds):", total_today_activity_time_seconds)
    print("Total Activity Time (seconds):", total_activity_time_seconds)

    # Pass the data to the template
    context = {
        'uid': uid,
        'student_data': student_data,
        'total_today_activity_time_hours': total_today_activity_time_hours,
        'total_today_activity_time_minutes': total_today_activity_time_minutes,
        'total_today_activity_time_seconds': total_today_activity_time_seconds,
        'total_today_calories': total_today_calories,
        'total_activity_time_hours': total_activity_time_hours,
        'total_activity_time_minutes': total_activity_time_minutes,
        'total_activity_time_seconds': total_activity_time_seconds,
        'total_calories': total_calories,
    }

    return render(request, 'smartmirror.html', context)
