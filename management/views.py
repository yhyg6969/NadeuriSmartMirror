from django.shortcuts import render, redirect
from .models import Student
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import requires_csrf_token

school_passwords = {
    "서울영남초등학교": "0000",
    "서울백석초등학교": "0000",
    # Add other schools and passwords as needed
}

def management(request):
    context = {'students': [], 'error_message': None, 'show_data': False}
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'filter_students':
            school = request.POST.get('school')
            password = request.POST.get('password')
            
            if school not in school_passwords or password != school_passwords[school]:
                context['error_message'] = 'Invalid password for the selected school.'
                return render(request, 'management.html', context)
            
            # Create or get the user
            user, created = User.objects.get_or_create(username=school)
            user.set_password(school_passwords[school])
            user.save()
            
            # Authenticate the user
            user = authenticate(request, username=school, password=password)
            
            # If the user is valid, log them in
            if user is not None:
                login(request, user)
                students = Student.objects.filter(school=school)
                context['students'] = students
                context['show_data'] = True
                return render(request, 'management.html', context)
            else:
                context['error_message'] = 'Authentication failed.'
                return render(request, 'management.html', context)
        
        elif request.user.is_authenticated:
            school = request.user.username  # Use the logged-in user's username as the school identifier

            if action == 'create':
                uid = request.POST.get('uid')
                name = request.POST.get('name')
                grade = request.POST.get('grade')
                class_num = request.POST.get('class_num')
                number = request.POST.get('number')
                gender = request.POST.get('gender') == '남자'
                Student.objects.create(uid=uid, name=name, school=school, grade=grade, class_num=class_num, number=number, gender=gender)
                return redirect('management')  # Redirect after successful creation
            
            elif action == 'update':
                uid = request.POST.get('uid')
                try:
                    student = Student.objects.get(uid=uid)
                except Student.DoesNotExist:
                    context['error_message'] = 'Student with given UID does not exist.'
                    return redirect('management')
                
                student.name = request.POST.get('name')
                student.school = school  # Keep the school consistent with the logged-in user's school
                student.grade = request.POST.get('grade')
                student.class_num = request.POST.get('class_num')
                student.number = request.POST.get('number')
                student.gender = request.POST.get('gender') == '남자'
                student.save()
                return redirect('management')  # Redirect after successful update
            
            elif action == 'delete':
                uid = request.POST.get('uid')
                try:
                    student = Student.objects.get(uid=uid)
                except Student.DoesNotExist:
                    context['error_message'] = 'Student with given UID does not exist.'
                    return redirect('management')
                student.delete()
                return redirect('management')  # Redirect after successful delete

            # After performing any CRUD operation, fetch the updated list of students
            students = Student.objects.filter(school=school)
            context['students'] = students
            context['show_data'] = True
    
    # Handle GET request
    if request.user.is_authenticated:
        school = request.user.username
        students = Student.objects.filter(school=school)
        context['students'] = students
        context['show_data'] = True

    return render(request, 'management.html', context)

@requires_csrf_token
def custom_csrf_failure(request, reason=""):
    return redirect(request.META.get('HTTP_REFERER', '/'))





