from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.timezone import localtime, now
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.hashers import make_password, check_password, get_random_string
from django.core.serializers.json import DjangoJSONEncoder

from .models import (
    user_table, center_table,
    paps_table, sprocket_table, teblow_table, dtx_table, smartmirror_table
)

from datetime import datetime, timedelta, timezone
import json

from collections import defaultdict


def logout_view(request):
    logout(request)
    return redirect('smartmirror:smartmirror')


def smartmirror(request):
    context = {'users': [], 'show_data': False, 'centers': center_table.objects.all()}
    print("🔍 smartmirror view accessed")

    if request.user.is_authenticated:
        center_name = request.user.username
        context['users'] = user_table.objects.filter(center_name=center_name)
        context['show_data'] = True

    if request.method == 'POST':
        content_type = request.META.get('CONTENT_TYPE', '')

        if 'application/json' in content_type:
            try:
                data = json.loads(request.body)
                action = data.get('action')

                if action == 'login':
                    center_name = data.get('center_name')
                    password = data.get('password')

                    if not center_name or not password:
                        return JsonResponse({"success": False, "message": "모든 필드를 입력해주세요."})

                    try:
                        center = center_table.objects.get(center_name=center_name)
                    except center_table.DoesNotExist:
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

                    if not check_password(password, center.center_password):
                        request.session['failed_attempts'] = request.session.get('failed_attempts', 0) + 1
                        request.session.modified = True

                        if request.session['failed_attempts'] >= 5:
                            lock_until = now() + timedelta(minutes=30)
                            request.session['lock_time'] = lock_until.isoformat()
                            return JsonResponse({
                                "success": False,
                                "message": f"비밀번호가 5회 틀렸습니다. {lock_until.strftime('%Y-%m-%d %H:%M:%S')}까지 다시 시도해주세요."
                            })

                        return JsonResponse({"success": False, "message": "비밀번호가 일치하지 않습니다."})

                    is_default_password = password == "000000"
                    user, created = User.objects.get_or_create(username=center_name)
                    user.set_password(password)
                    user.save()

                    user = authenticate(request, username=center_name, password=password)
                    if user:
                        login(request, user)
                        request.session['failed_attempts'] = 0
                        request.session['lock_time'] = None
                        request.session.save()

                        redirect_url = reverse('smartmirror:smartmirror')
                        return JsonResponse({
                            "success": True,
                            "message": "로그인 성공",
                            "redirect_url": redirect_url,
                            "default_password": is_default_password
                        })

            except Exception as e:
                return JsonResponse({"success": False, "message": "잘못된 요청 형식입니다."})

        else:
            action = request.POST.get('action')

            if action == 'create':
                uid = request.POST.get('uid', '').strip()
                user_name = request.POST.get('user_name', '').strip()
                center_name = request.POST.get('center_name', '').strip()
                birth = request.POST.get('birth', '').strip()
                gender_str = request.POST.get('gender')
                gender = True if gender_str == 'true' else False

                if not uid or not user_name or not birth or gender_str is None:
                    context['error_message'] = "모든 필드를 입력해 주세요."
                elif user_table.objects.filter(uid=uid).exists():
                    context['error_message'] = f"이미 존재하는 UID ({uid})입니다."
                else:
                    user_table.objects.create(uid=uid, user_name=user_name, center_name=center_name, birth=birth, gender=gender)

                if request.user.is_authenticated:
                    context['users'] = user_table.objects.filter(center_name=request.user.username)
                    context['show_data'] = True
                return render(request, 'smartmirror.html', context)

            elif action == 'update':
                uid = request.POST.get('uid', '').strip()
                user_name = request.POST.get('user_name', '').strip()
                birth = request.POST.get('birth', '').strip()
                gender_str = request.POST.get('gender')
                gender = True if gender_str == 'true' else False

                try:
                    user_obj = user_table.objects.get(uid=uid)
                    user_obj.user_name = user_name
                    user_obj.birth = birth
                    user_obj.gender = gender
                    user_obj.save()
                except user_table.DoesNotExist:
                    context['error_message'] = f"존재하지 않는 사용자입니다 (UID: {uid})"

                context['users'] = user_table.objects.filter(center_name=request.user.username)
                context['show_data'] = True
                return render(request, 'smartmirror.html', context)

            elif action == 'delete':
                uid = request.POST.get('uid', '').strip()
                try:
                    user_table.objects.filter(uid=uid).delete()
                except Exception as e:
                    context['error_message'] = f"삭제 중 오류 발생: {str(e)}"

                context['users'] = user_table.objects.filter(center_name=request.user.username)
                context['show_data'] = True
                return render(request, 'smartmirror.html', context)

    return render(request, 'smartmirror.html', context)



def inquiry(request):
    uid = request.GET.get('uid')
    if uid:
        try:
            user = user_table.objects.get(uid=uid)
        except user_table.DoesNotExist:
            return render(request, 'smartmirror.html', {'error_message': '사용자를 찾을 수 없습니다.'})

        tables = [paps_table, sprocket_table, teblow_table, dtx_table, smartmirror_table]
        date_set = set()

        for table in tables:
            for record in table.objects.filter(uid=uid):
                dt = datetime.fromtimestamp(record.start_ts, tz=timezone.utc).astimezone()
                date_set.add(dt.strftime('%Y-%m-%d'))

        context = {
            'user': user,
            'records_by_date': json.dumps(list(date_set), cls=DjangoJSONEncoder),  # JSON으로 변환
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
    end_ts = int(end_datetime.timestamp())

    all_tables = [
        paps_table, sprocket_table, teblow_table, dtx_table, smartmirror_table
    ]
    game_records = []

    for model in all_tables:
        records = model.objects.filter(uid=uid, start_ts__gte=start_ts, start_ts__lt=end_ts)
        game_records.extend(records)

    total_play_time = 0

    for game in game_records:
        game.start_time = datetime.fromtimestamp(game.start_ts, tz=timezone.utc)
        game.finish_time = datetime.fromtimestamp(game.finish_ts, tz=timezone.utc)
        game.play_time = getattr(game, 'play_time', (game.finish_time - game.start_time).total_seconds())
        game.minutes = int(game.play_time // 60)
        game.seconds = int(game.play_time % 60)
        total_play_time += game.play_time

    context = {
        'user': user,
        'game_records': game_records,
        'selected_date': start_datetime.date(),
        'total_play_hours': int(total_play_time // 3600),
        'total_play_minutes': int(total_play_time // 60),
        'total_play_seconds': int(total_play_time % 60),
    }

    return render(request, 'popup_modal2.html', context)


def custom_csrf_failure(request, reason=""):
    return redirect(request.META.get('HTTP_REFERER', '/'))


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('smartmirror:smartmirror')

    def form_valid(self, form):
        center_name = self.request.user.username
        try:
            center = center_table.objects.get(center_name=center_name)
            salt = get_random_string(16)
            raw_password = form.cleaned_data['new_password1']
            hashed_password = make_password(raw_password, salt=salt)

            center.center_password = hashed_password
            center.center_salt = salt
            center.save()
        except center_table.DoesNotExist:
            messages.error(self.request, "해당 기관을 찾을 수 없습니다.")
            return redirect('smartmirror:smartmirror')

        super().form_valid(form)
        logout(self.request)
        messages.success(self.request, "비밀번호가 성공적으로 변경되었습니다. 다시 로그인해 주세요.")
        return redirect('smartmirror:smartmirror')
