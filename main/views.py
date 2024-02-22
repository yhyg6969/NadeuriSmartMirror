from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, F
from datetime import datetime, timedelta
from django.utils import timezone
from .models import GameRecord, Student
from django.http import HttpResponse

def main(request):
    # Retrieve user information from the session
    user_info = request.session.get('user_info')

    if not user_info or 'uid' not in user_info:
        messages.error(request, 'User information not found. Please log in.')
        return render(request, 'main.html', {'user_info': None})

    # Retrieve uid from the session
    uid = user_info.get('uid')
    
    # Store uid and school in the session
    request.session['uid'] = uid
    
    # Query the database using uid to get user-specific data
    student_data = Student.objects.filter(uid=str(uid)).values().first()

    # Store school in the session
    request.session['school'] = student_data.get('school', None)

    # Query the game records for the specified UID
    start_time = int((timezone.now() - timedelta(days=365)).timestamp())
    end_time = int(timezone.now().timestamp())
    records = GameRecord.objects.filter(
        uid=uid,
        start_ts__gte=start_time,
        finish_ts__lte=end_time
    )

    # Calculate the total activity time in minutes and seconds
    total_activity_time_seconds = records.aggregate(total_time=Sum(F('finish_ts') - F('start_ts')))['total_time']

    if total_activity_time_seconds is None:
        total_activity_time_seconds = 0

    # Convert total_activity_time_seconds to a timedelta object
    total_activity_time = timedelta(seconds=int(total_activity_time_seconds))

    # Extract total_activity_time in minutes and seconds
    total_activity_time_minutes, total_activity_time_seconds = divmod(total_activity_time.seconds, 60)

    # Pass the data to the template
    context = {
        'user_info': user_info,
        'student_data': student_data,
        'records': records,
        'total_activity_time_minutes': total_activity_time_minutes,
        'total_activity_time_seconds': total_activity_time_seconds,
    }

    return render(request, 'main.html', context)

def popup_modal(request):
    try:
        # Retrieve parameters from the URL
        year = request.GET.get('year')
        month = request.GET.get('month')
        day = request.GET.get('day')

        # Validate date parameters
        if year is None or month is None or day is None:
            raise ValueError("Invalid or missing date parameters")

        # Retrieve UID from the user session
        user_info = request.session.get('user_info')
        if not user_info or 'uid' not in user_info:
            raise ValueError("User information not found in the session")

        # Convert date parameters to timestamp range
        start_timestamp = int(datetime(int(year), int(month), int(day), 0, 0).timestamp())
        end_timestamp = int(datetime(int(year), int(month), int(day), 23, 59, 59).timestamp())

        # Retrieve UID from the session
        uid = user_info.get('uid')

        # Query the database using timestamp range and UID
        records = GameRecord.objects.filter(uid=uid, start_ts__gte=start_timestamp, finish_ts__lte=end_timestamp)

        # Check if there are matching records
        if not records.exists():
            # No records found for the specified date, render a response with an error message
            error_message = "해당 날짜에 기록된 활동이 없습니다"
            return render(request, 'popup_modal.html', {'error_message': error_message})

        # Calculate total activity time in seconds
        total_activity_time_seconds = records.aggregate(total_time=Sum(F('finish_ts') - F('start_ts')))['total_time'] or 0

        # Convert total_activity_time_seconds to a timedelta object
        total_activity_time = timedelta(seconds=int(total_activity_time_seconds))

        # Extract total_activity_time in hours, minutes, and seconds
        total_hours, remainder = divmod(total_activity_time.seconds, 3600)
        total_minutes, total_seconds = divmod(remainder, 60)

        # Calculate total calories
        total_calories = (total_activity_time_seconds / 60) * 7

        # Pass the data to the template
        context = {
            'year': year,
            'month': month,
            'day': day,
            'records': records,
            'total_hours': total_hours,
            'total_minutes': total_minutes,
            'total_seconds': total_seconds,
            'total_calories': total_calories,
        }

        # Render the template
        return render(request, 'popup_modal.html', context)

    except Exception as e:
        # Handle other exceptions and return an error response
        error_message = str(e)
        return HttpResponse(f"{error_message}", status=500)