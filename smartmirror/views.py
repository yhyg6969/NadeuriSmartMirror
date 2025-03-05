from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import user_table, game_table, walk_table, stretch_table, center_table
from datetime import datetime, timezone, timedelta

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

def smartmirror(request):
    context = {'users': [], 'show_data': False, 'centers': center_table.objects.all()}

    if request.user.is_authenticated:
        center_name = request.user.username
        context['users'] = user_table.objects.filter(center_name=center_name)
        context['show_data'] = True  # Ensure data is displayed after refresh

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            center_name = request.POST.get('center_name')
            password = request.POST.get('password')

            if not center_name or not password:
                context['error_message'] = '모든 필드를 입력해주세요.'
                return render(request, 'smartmirror.html', context)

            try:
                center = center_table.objects.get(center_name=center_name)
            except center_table.DoesNotExist:
                context['error_message'] = '존재하지 않는 기관입니다.'
                return render(request, 'smartmirror.html', context)

            if password != center.center_password:
                context['error_message'] = '비밀번호가 일치하지 않습니다.'
                return render(request, 'smartmirror.html', context)

            # Authenticate user
            user, created = User.objects.get_or_create(username=center_name)
            user.set_password(password)
            user.save()

            user = authenticate(request, username=center_name, password=password)
            if user is not None:
                login(request, user)
                context['users'] = user_table.objects.filter(center_name=center_name)
                context['show_data'] = True
                return redirect('smartmirror:smartmirror')

        elif action in ['create', 'update', 'delete'] and request.user.is_authenticated:
            center_name = request.user.username

            if action == 'create':
                uid = request.POST.get('uid')
                user_name = request.POST.get('user_name')
                birth = request.POST.get('birth')
                gender = request.POST.get('gender') == 'true'

                if not uid or not user_name or not birth:
                    context['error_message'] = '모든 필드를 입력해주세요.'
                    return render(request, 'smartmirror.html', context)

                if user_table.objects.filter(uid=uid).exists():
                    context['error_message'] = '중복된 UID입니다.'
                    return render(request, 'smartmirror.html', context)

                user_table.objects.create(uid=uid, user_name=user_name, center_name=center_name, birth=birth, gender=gender)

            elif action == 'update':
                uid = request.POST.get('uid')
                user_name = request.POST.get('user_name')
                birth = request.POST.get('birth')
                gender = request.POST.get('gender') == 'true'
                center_name = request.POST.get('center_name')

                if not uid or not user_name or not birth:
                    context['error_message'] = '모든 필드를 입력해주세요.'
                    return render(request, 'smartmirror.html', context)

                user = user_table.objects.get(uid=uid)
                user.user_name = user_name
                user.birth = birth
                user.gender = gender
                user.center_name = center_name
                user.save()

            elif action == 'delete':
                uid = request.POST.get('uid')
                user_table.objects.filter(uid=uid).delete()

            return redirect('smartmirror:smartmirror')

    return render(request, 'smartmirror.html', context)


def inquiry(request):
    uid = request.GET.get('uid')
    if uid:
        try:
            user = user_table.objects.get(uid=uid)
            games = game_table.objects.filter(uid=uid)
            walks = walk_table.objects.filter(uid=uid)
            stretches = stretch_table.objects.filter(uid=uid)
        except user_table.DoesNotExist:
            return render(request, 'smartmirror.html', {'error_message': 'User not found.'})
        
        context = {
            'user': user,
            'games': games,
            'walks': walks,
            'stretches': stretches,
        }
        
        return render(request, 'inquiry.html', context)
    
    return redirect('smartmirror:smartmirror')

def popup_modal(request):
    uid = request.GET.get('uid')
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    
    if not uid or not year or not month or not day:
        return HttpResponse('Missing parameters.', status=400)
    
    try:
        user = user_table.objects.get(uid=uid)
    except user_table.DoesNotExist:
        return HttpResponse('User not found.', status=404)
    
    # Convert year, month, day to integers
    year = int(year)
    month = int(month)
    day = int(day)
    
    # Calculate start and end datetime objects for the selected day
    start_datetime = datetime(year, month, day, 0, 0, 0, tzinfo=timezone.utc)
    end_datetime = start_datetime + timedelta(days=1)

    # Convert datetime objects to timestamps
    start_ts = int(start_datetime.timestamp())
    end_ts = int(end_datetime.timestamp()) - 1

    # Filter game records for the selected date
    game_records = game_table.objects.filter(
        uid=uid,
        start_ts__gte=start_ts,
        start_ts__lt=end_ts,
    )
    
    for game in game_records:
        game.minutes = game.play_time // 60
        game.seconds = game.play_time % 60
        game.start_time = datetime.fromtimestamp(game.start_ts)
        game.finish_time = datetime.fromtimestamp(game.finish_ts)
        if game.game_type == 4:
            activity_duration = game.finish_time - game.start_time
            game.activity_seconds = int(activity_duration.total_seconds())  # Total seconds
            game.activity_minutes = int(activity_duration.total_seconds() // 60)  # Minutes




    # Filter walk records for the selected date
    walk_records = walk_table.objects.filter(
        uid=uid,
        start_ts__gte=start_ts,
        start_ts__lt=end_ts,
    )

    for walk in walk_records:
        walk.minutes = walk.walk_time // 60
        walk.seconds = walk.walk_time % 60
        walk.start_time = datetime.fromtimestamp(walk.start_ts)

    # Filter stretch records for the selected date
    stretch_records = stretch_table.objects.filter(
        uid=uid,
        start_ts__gte=start_ts,
        start_ts__lt=end_ts,
    )

    for stretch in stretch_records:
        stretch.minutes = stretch.stretch_time // 60
        stretch.seconds = stretch.stretch_time % 60
        stretch.start_time = datetime.fromtimestamp(stretch.start_ts)

    
    context = {
        'user': user,
        'game_records': game_records,
        'walk_records': walk_records,
        'stretch_records': stretch_records,
        'selected_date': start_datetime.date(),  # Pass the selected date object
    }
    
    return render(request, 'popup_modal2.html', context)

def custom_csrf_failure(request, reason=""):
    return redirect(request.META.get('HTTP_REFERER', '/'))



class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('smartmirror:password_change_done')

    def form_valid(self, form):
        # Get the current user (assuming the user's username is the center_name in the center_table)
        center_name = self.request.user.username
        try:
            # Find the center record corresponding to the current user
            center = center_table.objects.get(center_name=center_name)
            # Update the password field
            center.center_password = form.cleaned_data['new_password1']  # New password entered by the user
            center.save()  # Save the updated center record
        except center_table.DoesNotExist:
            # Handle the case if the center record is not found
            messages.error(self.request, "해당 기관을 찾을 수 없습니다.")
            return redirect('smartmirror:smartmirror')

        # Call the parent form_valid method to save the password for the user and send success message
        response = super().form_valid(form)
        messages.success(self.request, "비밀번호가 성공적으로 변경되었습니다.")  # Show the success message
        return response

