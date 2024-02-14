from django.shortcuts import render
from django.contrib import messages
from django.db.models import Sum, F
from datetime import timedelta
from django.utils import timezone
from .models import GameRecord, Student

def Xplaywall(request):
    uid = request.session.get('uid', None)

    if not uid:
        messages.error(request, 'User information not found. Please log in.')
        return render(request, 'Xplaywall.html', {'user_info': None})

    # Query the database using uid to get user-specific data
    student_data = Student.objects.filter(uid=str(uid)).values().first()

    # Calculate today's total activity time and calories for 'game1'
    start_time_today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_time_today = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)

    records_today_game1 = GameRecord.objects.filter(
        uid=uid,
        game_type='game1',  # Filter for 'game1'
        start_ts__range=(start_time_today.timestamp(), end_time_today.timestamp())
    )

    total_today_activity_time_seconds_game1 = sum(record.finish_ts - record.start_ts for record in records_today_game1)
    total_today_calories_game1 = (total_today_activity_time_seconds_game1 / 60) * 7

    total_today_activity_time_game1 = timedelta(seconds=int(total_today_activity_time_seconds_game1))
    total_today_activity_time_hours_game1, remainder = divmod(total_today_activity_time_game1.seconds, 3600)
    total_today_activity_time_minutes_game1, total_today_activity_time_seconds_game1 = divmod(remainder, 60)

    # Query the game records for 'game1' and the specified UID (total activity time and calories)
    start_time = timezone.now() - timedelta(days=365)
    end_time = timezone.now()

    records_game1 = GameRecord.objects.filter(
        uid=uid,
        game_type='game1',  # Filter for 'game1'
        start_ts__range=(start_time.timestamp(), end_time.timestamp())
    )

    total_activity_time_seconds_game1 = sum(record.finish_ts - record.start_ts for record in records_game1)
    total_calories_game1 = (total_activity_time_seconds_game1 / 60) * 7

    total_activity_time_game1 = timedelta(seconds=int(total_activity_time_seconds_game1))
    total_activity_time_hours_game1, remainder = divmod(total_activity_time_game1.seconds, 3600)
    total_activity_time_minutes_game1, total_activity_time_seconds_game1 = divmod(remainder, 60)

    # Pass the data to the template
    context = {
        'uid': uid,
        'student_data': student_data,
        'total_today_activity_time_hours': total_today_activity_time_hours_game1,
        'total_today_activity_time_minutes': total_today_activity_time_minutes_game1,
        'total_today_activity_time_seconds': total_today_activity_time_seconds_game1,
        'total_today_calories': total_today_calories_game1,
        'total_activity_time_hours': total_activity_time_hours_game1,
        'total_activity_time_minutes': total_activity_time_minutes_game1,
        'total_activity_time_seconds': total_activity_time_seconds_game1,
        'total_calories': total_calories_game1,
    }

    return render(request, 'Xplaywall.html', context)
