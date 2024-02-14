from django.shortcuts import render, redirect, get_object_or_404
from .models import Student

def management(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        uid = request.POST.get('uid')
        if action == 'create':
            name = request.POST.get('name')
            school = request.POST.get('school')
            grade = request.POST.get('grade')
            class_num = request.POST.get('class_num')
            number = request.POST.get('number')
            gender = bool(request.POST.get('gender'))
            Student.objects.create(uid=uid, name=name, school=school, grade=grade, class_num=class_num, number=number, gender=gender)
        elif action == 'update':
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
            try:
                student = Student.objects.get(uid=uid)
            except Student.DoesNotExist:
                # Handle case when student with given UID doesn't exist
                return redirect('management')
            student.delete()
        return redirect('management')
    else:
        students = Student.objects.all()
        return render(request, 'management.html', {'students': students})
