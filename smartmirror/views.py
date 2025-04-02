from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import user_table, game_table, walk_table, stretch_table, center_table
from datetime import datetime, timedelta, timezone
import datetime as dt
from django.utils.timezone import localtime, now
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
import json
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

def smartmirror(request):
    context = {'users': [], 'show_data': False, 'centers': center_table.objects.all()}
    
    print("🔍 smartmirror view accessed")  # 디버깅용 로그
    
    if request.user.is_authenticated:
        center_name = request.user.username
        print(f"✅ User authenticated: {center_name}")
        context['users'] = user_table.objects.filter(center_name=center_name)
        context['show_data'] = True

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            print(f"🔍 Received action: {action}")
            
            if action == 'login':
                center_name = data.get('center_name')
                password = data.get('password')
                print(f"🔍 Login attempt - center_name: {center_name}, password: {password}")

                if not center_name or not password:
                    return JsonResponse({"success": False, "message": "모든 필드를 입력해주세요."})
                
                try:
                    center = center_table.objects.get(center_name=center_name)
                except center_table.DoesNotExist:
                    print("❌ Center not found")
                    return JsonResponse({"success": False, "message": "존재하지 않는 기관입니다."})
                
                lock_time = request.session.get('lock_time')
                if lock_time:
                    if isinstance(lock_time, str):
                        lock_time = parse_datetime(lock_time)
                    if lock_time and lock_time > now():
                        kst_lock_time = localtime(lock_time)
                        return JsonResponse({
                            "success": False,
                            "message": f"계정이 잠겼습니다. {kst_lock_time.strftime('%Y-%m-%d %H:%M:%S')}까지 기다려주세요."
                        })
                
                if password != center.center_password:
                    request.session['failed_attempts'] = request.session.get('failed_attempts', 0) + 1
                    request.session.modified = True
                    print(f"❌ Password mismatch - Attempt {request.session['failed_attempts']}")
                    
                    if request.session['failed_attempts'] >= 5:
                        lock_until = now() + timedelta(minutes=30)
                        request.session['lock_time'] = lock_until.isoformat()
                        print(f"🔒 Account locked until {lock_until}")
                        return JsonResponse({
                            "success": False,
                            "message": f"비밀번호가 5회 틀렸습니다. {lock_until.strftime('%Y-%m-%d %H:%M:%S')}까지 다시 시도해주세요."
                        })
                    return JsonResponse({"success": False, "message": "비밀번호가 일치하지 않습니다."})
                
                user, created = User.objects.get_or_create(username=center_name)
                user.set_password(password)
                user.save()
                
                user = authenticate(request, username=center_name, password=password)
                print(f"🔍 Authenticated user: {user}")
                
                if user is not None:
                    login(request, user)
                    request.session['failed_attempts'] = 0
                    request.session['lock_time'] = None
                    request.session.save()

                    # 로그인 성공 시, UID 확인 및 리디렉션
                    user_obj = user_table.objects.filter(center_name=center_name).first()
                    uid = user_obj.uid if user_obj else None  # None을 반환하여 빈 값 방지
                    redirect_url = reverse('smartmirror:smartmirror')
                    
                    # uid가 있을 경우 URL에 추가
                    if uid:
                        redirect_url += f'?uid={uid}'

                    return JsonResponse({"success": True, "message": "로그인 성공", "redirect_url": redirect_url})


                
            elif action == 'create':
                uid = data.get('uid')
                user_name = data.get('user_name')
                birth = data.get('birth')
                gender = data.get('gender') == 'true'
                
                print(f"🔍 Creating user - UID: {uid}, Name: {user_name}, Birth: {birth}, Gender: {gender}")
                
                if not uid or not user_name or not birth:
                    return JsonResponse({"success": False, "message": "모든 필드를 입력해주세요."})
                
                if user_table.objects.filter(uid=uid).exists():
                    print("❌ Duplicate UID")
                    return JsonResponse({"success": False, "message": "중복된 UID입니다."})
                
                user_table.objects.create(uid=uid, user_name=user_name, center_name=center_name, birth=birth, gender=gender)
                print("✅ User created successfully")
                return JsonResponse({"success": True, "message": "사용자 생성 완료"})
                
            elif action == 'update':
                uid = data.get('uid')
                user_name = data.get('user_name')
                birth = data.get('birth')
                gender = data.get('gender') == 'true'
                
                print(f"🔍 Updating user - UID: {uid}")
                
                if not uid or not user_name or not birth:
                    return JsonResponse({"success": False, "message": "모든 필드를 입력해주세요."})
                
                user = user_table.objects.get(uid=uid)
                user.user_name = user_name
                user.birth = birth
                user.gender = gender
                user.save()
                print("✅ User updated successfully")
                return JsonResponse({"success": True, "message": "사용자 정보 수정 완료"})
                
            elif action == 'delete':
                uid = data.get('uid')
                print(f"🔍 Deleting user - UID: {uid}")
                
                user_table.objects.filter(uid=uid).delete()
                print("✅ User deleted successfully")
                return JsonResponse({"success": True, "message": "사용자 삭제 완료"})
                
        except json.JSONDecodeError:
            print("❌ JSON Decode Error")
            return JsonResponse({"success": False, "message": "잘못된 요청 형식입니다."})
    
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
    
    if not all([uid, year, month, day]):
        return HttpResponse('Missing parameters.', status=400)
    
    try:
        user = user_table.objects.get(uid=uid)
    except user_table.DoesNotExist:
        return HttpResponse('User not found.', status=404)

    try:
        year, month, day = map(int, [year, month, day])
        start_datetime = datetime(year, month, day, 0, 0, 0, tzinfo=timezone.utc)
        end_datetime = start_datetime + timedelta(days=1)
    except ValueError:
        return HttpResponse('Invalid date format.', status=400)

    start_ts = int(start_datetime.timestamp())
    end_ts = int(end_datetime.timestamp()) - 1

    game_records = game_table.objects.filter(uid=uid, start_ts__gte=start_ts, start_ts__lt=end_ts)
    walk_records = walk_table.objects.filter(uid=uid, start_ts__gte=start_ts, start_ts__lt=end_ts)
    stretch_records = stretch_table.objects.filter(uid=uid, start_ts__gte=start_ts, start_ts__lt=end_ts)

    total_play_time = 0  # To accumulate total play time

    for game in game_records:
        game.start_time = datetime.fromtimestamp(game.start_ts, tz=timezone.utc)
        game.finish_time = datetime.fromtimestamp(game.finish_ts, tz=timezone.utc)

        # Calculate total play time if not already stored
        if hasattr(game, 'play_time'):
            game.minutes = game.play_time // 60
            game.seconds = game.play_time % 60
            total_play_time += game.play_time  # Accumulate total play time
        else:
            game.play_time = (game.finish_time - game.start_time).total_seconds()
            game.minutes = int(game.play_time // 60)
            game.seconds = int(game.play_time % 60)
            total_play_time += game.play_time  # Accumulate total play time

        # Debugging prints (Check values in logs)
        print(f"Game {game.record_id}: Start {game.start_time}, Finish {game.finish_time}, Play Time {game.play_time}")

        if game.game_type == "4":  # Ensure correct type comparison
            game.activity_seconds = int(game.play_time)
            game.activity_minutes = game.activity_seconds // 60

    # Convert total play time to minutes and seconds
    total_play_hours = int(total_play_time // 3600)
    total_play_minutes = int(total_play_time // 60)
    total_play_seconds = int(total_play_time % 60)

    for walk in walk_records:
        walk.start_time = datetime.fromtimestamp(walk.start_ts, tz=timezone.utc)
        walk.minutes = walk.walk_time // 60
        walk.seconds = walk.walk_time % 60

    for stretch in stretch_records:
        stretch.start_time = datetime.fromtimestamp(stretch.start_ts, tz=timezone.utc)
        stretch.minutes = stretch.stretch_time // 60
        stretch.seconds = stretch.stretch_time % 60

    context = {
        'user': user,
        'game_records': game_records,
        'walk_records': walk_records,
        'stretch_records': stretch_records,
        'selected_date': start_datetime.date(),
        'total_play_hours': total_play_hours, 
        'total_play_minutes': total_play_minutes,  # Send total play time to template
        'total_play_seconds': total_play_seconds,
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
