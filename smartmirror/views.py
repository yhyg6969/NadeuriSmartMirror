from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import user_table, game_table, walk_table, stretch_table
from datetime import datetime, timezone, timedelta

def smartmirror(request):
    context = {'users': [], 'show_data': False}
    
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
                "광진구 치매안심센터": "0000",
                "영등포구 치매안심센터": "0000",
                "금천구 치매안심센터": "0000",
                "광진구 치매안심센터": "0000",
                "중구 치매안심센터": "3400",
                "강서구 치매안심센터": "gs090901",
                "중랑구 치매안심센터": "0000",
                "도봉구 치매안심센터": "0000",
                "구로구 치매안심센터": "0000",
                "양천구 치매안심센터": "0000",
                "용산구 치매안심센터": "0000",
                "관악구 치매안심센터": "0000",
                "동작구 치매안심센터": "0000",
                "노원구 치매안심센터": "0000",
                "은평구 치매안심센터": "0000",
                "마포구 치매안심센터": "0000",
                "종로구 치매안심센터": "0000",
                "강북구 치매안심센터": "0000",
                "강북노인종합복지관": "0000",
                "서대문노인종합복지관": "0000",
                "우리마포복지관": "0000",
                "노원노인종합복지관": "0000",
                "광진노인종합복지관": "0000",
                "마포노인종합복지관": "0000",
                "강서노인종합복지관": "0000",
                "용산노인종합복지관": "0000",
                "성가정노인종합복지관": "0000",
                "구로노인종합복지관": "0000",
                "은평노인종합복지관": "0000",
                "도봉노인종합복지관": "0000",
                "금천노인종합복지관": "0000",
                "성동노인종합복지관": "0000",
                "서울노인복지센터": "0000",
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
                
                # Check if the UID already exists
                if user_table.objects.using('secondary').filter(uid=uid).exists():
                    context['error_message'] = '중복된 UID 입니다.'
                    context['popup_alert'] = True  # Flag to show popup alert
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
                    users = user_table.objects.using('secondary').filter(center_name=center_name)
                    context['users'] = users
                    context['show_data'] = True
                    return render(request, 'smartmirror.html', context)

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
                
                # Check if the new UID already exists (only if it's being changed)
                new_uid = request.POST.get('new_uid')
                if new_uid and new_uid != uid and user_table.objects.using('secondary').filter(uid=new_uid).exists():
                    context['error_message'] = '중복된 UID 입니다'
                    context['popup_alert'] = True  # Flag to show popup alert
                    users = user_table.objects.using('secondary').filter(center_name=center_name)
                    context['users'] = users
                    context['show_data'] = True
                    return render(request, 'smartmirror.html', context)
                
                if new_uid:
                    user.uid = new_uid

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
                    users = user_table.objects.using('secondary').filter(center_name=center_name)
                    context['users'] = users
                    context['show_data'] = True
                    return render(request, 'smartmirror.html', context)
                
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
    
    for game in game_records:
        game.minutes = game.play_time // 60
        game.seconds = game.play_time % 60
        game.start_time = datetime.fromtimestamp(game.start_ts)
        game.finish_time = datetime.fromtimestamp(game.finish_ts)

        # Calculate total activity time for game_type 4
        if game.game_type == 4:
            activity_duration = game.finish_time - game.start_time
            game.activity_minutes = int(activity_duration.total_seconds() // 60)


    # Filter walk records for the selected date
    walk_records = walk_table.objects.using('secondary').filter(
        uid=uid,
        start_ts__gte=start_ts,
        start_ts__lt=end_ts,
    )

    for walk in walk_records:
        walk.minutes = walk.walk_time // 60
        walk.seconds = walk.walk_time % 60
        walk.start_time = datetime.fromtimestamp(walk.start_ts)

    # Filter stretch records for the selected date
    stretch_records = stretch_table.objects.using('secondary').filter(
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




