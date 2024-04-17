from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from .models import Paps, Student

def paps(request):
    uid = request.session.get('uid', None)

    if not uid:
        messages.error(request, 'User information not found. Please log in.')
        return render(request, 'paps.html', {'user_info': None})

    # Fetch student data
    student_data = Student.objects.filter(uid=uid).first()

    # Fetch all unique game types and sort them by their number
    game_types = Paps.objects.values_list('game_type', flat=True).distinct()
    game_types = sorted(game_types, key=lambda game_type: int(game_type.replace('paps', '')))

    # Initialize context with student data
    context = {
        'uid': uid,
        'student_data': student_data,
        'games': [],
    }

    # Fetch records for each game type
    for game_type in game_types:
        # Fetch all records for the user and the game type
        records = Paps.objects.filter(uid=uid, game_type=game_type)

        # Initialize today's record as None
        today_record = None

        # Initialize highest record as None
        highest_record = None

        # Initialize recent records as an empty list
        recent_records = []

        # Iterate over the records
        for record in records:
            # Convert the start_ts to a datetime object
            start_ts = datetime.fromtimestamp(record.start_ts)

            # Check if the record is from today
            if start_ts.date() == timezone.now().date():
                today_record = record

            # Check if the record is the highest one
            if highest_record is None or record.score > highest_record.score:
                highest_record = record

            # Add the record to the recent records
            recent_records.append(record)

        # Sort the records by start_ts in descending order and keep only the 3 most recent ones
        recent_records = sorted(recent_records, key=lambda record: record.start_ts, reverse=True)[:3]

        # Add the records to the context
        context['games'].append({
            'game_type': game_type,
            'today_record': today_record,
            'highest_record': highest_record,
            'recent_records': recent_records,
        })

    return render(request, 'paps.html', context)