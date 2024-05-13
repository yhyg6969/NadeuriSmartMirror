from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student

# Define passwords for each school
school_passwords = {
    "서울영남초등학교": "0000",
    "서울백석초등학교": "0000",
    # Add other schools and passwords as needed
}

def management(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'filter_students':
            school = request.POST.get('school')
            password = request.POST.get('password')
            # Check if password is correct for the selected school
            if school not in school_passwords or password != school_passwords[school]:
                messages.error(request, '비밀번호가 일치하지 않습니다')
                return redirect('management')
            # Filter students based on school
            students = Student.objects.filter(school=school)
            return render(request, 'management.html', {'students': students, 'error_message': None})
        elif action == 'create':
            name = request.POST.get('name')
            school = request.POST.get('school')
            grade = request.POST.get('grade')
            class_num = request.POST.get('class_num')
            number = request.POST.get('number')
            gender = bool(request.POST.get('gender'))
            Student.objects.create(uid=uid, name=name, school=school, grade=grade, class_num=class_num, number=number, gender=gender)
        elif action == 'update':
            uid = request.POST.get('uid')
            try:
                student = Student.objects.get(uid=uid)
            except Student.DoesNotExist:
                # Handle case when student with given UID doesn't exist
                return redirect('management')
            student.uid = request.POST.get('uid')
            student.name = request.POST.get('name')
            student.school = request.POST.get('school')
            student.grade = request.POST.get('grade')
            student.class_num = request.POST.get('class_num')
            student.number = request.POST.get('number')
            student.gender = bool(request.POST.get('gender'))
            student.save()
        elif action == 'delete':
            uid = request.POST.get('uid')
            try:
                student = Student.objects.get(uid=uid)
            except Student.DoesNotExist:
                # Handle case when student with given UID doesn't exist
                return redirect('management')
            student.delete()
        return redirect('management')
    else:
        students = Student.objects.all()
        return render(request, 'management.html', {'students': students, 'error_message': None})

