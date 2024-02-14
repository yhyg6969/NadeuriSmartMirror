# login/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from .forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            school = form.cleaned_data['school']
            password = form.cleaned_data['password']

            students = Student.objects.filter(school=school)

            if students.exists():
                for student in students:
                    if password == student.generate_password():
                        # Store only 'uid' in session
                        request.session['user_info'] = {'uid': student.uid}

                        # Successful login
                        return redirect('main')  # Update with your actual redirect URL

                else:
                    messages.error(request, '로그인에 실패했습니다. 학교와 번호를 다시 확인해주세요.')

            else:
                messages.error(request, '로그인에 실패했습니다. 학교와 번호를 다시 확인해주세요.')

            # Clear all messages
            messages.success(request, '')
            messages.error(request, '')

            return render(request, 'login.html', {'form': form, 'alert_messages': True})

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'alert_messages': False})
