from django.shortcuts import render
from django.contrib import messages
from django.db.models import Sum, F
from datetime import timedelta
from .models import GameRecord, Student

def ranking(request):
    uid = request.session.get('uid', None)
    school = request.session.get('school', None)

    # Fetch user data to pass to the template
    student_data = None
    if uid and school:
        student_data = Student.objects.filter(uid=str(uid)).values().first()

    if not uid or not school:
        messages.error(request, 'User information not found. Please log in.')
        return render(request, 'ranking.html', {'user_info': None, 'student_data': student_data})

    # Query all students from the database
    all_students = Student.objects.filter(school=school)

    # Calculate total activity time for each student
    student_activity_times = {}
    for student in all_students:
        # Query game records for each student
        records = GameRecord.objects.filter(uid=student.uid)
        total_activity_time = records.aggregate(total_time=Sum(F('finish_ts') - F('start_ts')))['total_time'] or 0
        # Convert total activity time to a timedelta object
        total_activity_time_timedelta = timedelta(seconds=total_activity_time)
        student_activity_times[student] = total_activity_time_timedelta

    # Sort students by total activity time
    sorted_students = sorted(student_activity_times.items(), key=lambda x: x[1], reverse=True)

    # Separate top3 and ranked students
    top3_students = sorted_students[:3]
    ranked_students = sorted_students[3:]

    # Reorder top3_students so that 2nd place comes first
    if len(top3_students) >= 2:
        second_place_student = top3_students[1]
        top3_students.remove(second_place_student)
        top3_students.insert(0, second_place_student)

    # Pass the data to the template
    context = {
        'uid': uid,
        'school': school,
        'top3_students': [{'uid': student.uid, 'name': student.name, 'total_activity_time': time,
                           'hours_part': time.seconds // 3600, 'minutes_part': (time.seconds // 60) % 60}
                          for student, time in top3_students],
        'ranked_students': [{'uid': student.uid, 'name': student.name, 'total_activity_time': time,
                             'hours_part': time.seconds // 3600, 'minutes_part': (time.seconds // 60) % 60}
                            for student, time in ranked_students],
        'student_data': student_data,
    }

    return render(request, 'ranking.html', context)
