from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponse
from .models import user_table, game_table, walk_table, stretch_table
from datetime import datetime, timezone, timedelta


def smartmirror(request):
    context = {'users': [], 'error_message': None, 'show_data': False}
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'login':
            center_name = request.POST.get('center_name')
            password = request.POST.get('password')
            
            if not center_name or not password:
                context['error_message'] = '양식에 알맞게 입력해주세요'
                return render(request, 'smartmirror.html', context)
            
            center_passwords = {
                "동대문구 치매안심센터": "0000",
                "서대문구 치매안심센터": "0000",
                "서초구 치매안심센터": "0000",
                "성동구 치매안심센터": "0000",
                "성북구 치매안심센터": "0000",
                # Add other centers and passwords as needed
            }
            
            if center_name not in center_passwords or password != center_passwords[center_name]:
                context['error_message'] = 'Invalid password for the selected center.'
                return render(request, 'smartmirror.html', context)
            
            # Create or get the user
            user, created = User.objects.get_or_create(username=center_name)
            user.set_password(center_passwords[center_name])
            user.save()
            
            # Authenticate the user
            user = authenticate(request, username=center_name, password=password)
            
            # If the user is valid, log them in
            if user is not None:
                login(request, user)
                users = user_table.objects.using('secondary').filter(center_name=center_name)
                context['users'] = users
                context['show_data'] = True
                return render(request, 'smartmirror.html', context)
            else:
                context['error_message'] = 'Authentication failed.'
                return render(request, 'smartmirror.html', context)
        
        elif request.user.is_authenticated:
            center_name = request.user.username

            if action == 'create':
                uid = request.POST.get('uid')
                user_name = request.POST.get('user_name')
                birth = request.POST.get('birth')
                gender = request.POST.get('gender') == 'true'
                
                if not uid or not user_name or not birth:
                    context['error_message'] = '양식에 알맞게 입력해주세요'
                    users = user_table.objects.using('secondary').filter(center_name=center_name)
                    context['users'] = users
                    context['show_data'] = True
                    return render(request, 'smartmirror.html', context)
                
                user_table.objects.using('secondary').create(uid=uid, user_name=user_name, center_name=center_name, birth=birth, gender=gender)
                return redirect('smartmirror:smartmirror')
            
            elif action == 'update':
                uid = request.POST.get('uid')
                
                if not uid:
                    context['error_message'] = '양식에 알맞게 입력해주세요'
                    users = user_table.objects.using('secondary').filter(center_name=center_name)
                    context['users'] = users
                    context['show_data'] = True
                    return render(request, 'smartmirror.html', context)
                
                try:
                    user = user_table.objects.using('secondary').get(uid=uid)
                except user_table.DoesNotExist:
                    context['error_message'] = 'User with given UID does not exist.'
                    return redirect('smartmirror:smartmirror')
                
                user.user_name = request.POST.get('user_name')
                user.center_name = center_name
                user.birth = request.POST.get('birth')
                user.gender = request.POST.get('gender') == 'true'
                
                if not user.user_name or not user.birth:
                    context['error_message'] = '양식에 알맞게 입력해주세요'
                    users = user_table.objects.using('secondary').filter(center_name=center_name)
                    context['users'] = users
                    context['show_data'] = True
                    return render(request, 'smartmirror.html', context)
                
                user.save(using='secondary')
                return redirect('smartmirror:smartmirror')
            
            elif action == 'delete':
                uid = request.POST.get('uid')
                
                if not uid:
                    context['error_message'] = '양식에 알맞게 입력해주세요'
                    users = user_table.objects.using('secondary').filter(center_name=center_name)
                    context['users'] = users
                    context['show_data'] = True
                    return render(request, 'smartmirror.html', context)
                
                try:
                    user = user_table.objects.using('secondary').get(uid=uid)
                except user_table.DoesNotExist:
                    context['error_message'] = 'User with given UID does not exist.'
                    return redirect('smartmirror:smartmirror')
                user.delete(using='secondary')
                return redirect('smartmirror:smartmirror')
            
            # After performing any CRUD operation, fetch the updated list of users
            users = user_table.objects.using('secondary').filter(center_name=center_name)
            context['users'] = users
            context['show_data'] = True
    
    # Handle GET request
    if request.user.is_authenticated:
        center_name = request.user.username
        users = user_table.objects.using('secondary').filter(center_name=center_name)
        context['users'] = users
        context['show_data'] = True

    return render(request, 'smartmirror.html', context)

def inquiry(request):
    uid = request.GET.get('uid')
    if uid:
        try:
            user = user_table.objects.using('secondary').get(uid=uid)
            games = game_table.objects.using('secondary').filter(uid=uid)
            walks = walk_table.objects.using('secondary').filter(uid=uid)
            stretches = stretch_table.objects.using('secondary').filter(uid=uid)
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
        user = user_table.objects.using('secondary').get(uid=uid)
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
    game_records = game_table.objects.using('secondary').filter(
        uid=uid,
        start_ts__gte=start_ts,
        start_ts__lt=end_ts,
    )

    # Filter walk records for the selected date
    walk_records = walk_table.objects.using('secondary').filter(
        uid=uid,
        start_ts__gte=start_ts,
        start_ts__lt=end_ts,
    )

    # Filter stretch records for the selected date
    stretch_records = stretch_table.objects.using('secondary').filter(
        uid=uid,
        start_ts__gte=start_ts,
        start_ts__lt=end_ts,
    )

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




