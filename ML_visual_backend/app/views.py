import json

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        email = data['email']

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': '用户名已存在'}, status=400)

        hashed_password = make_password(password)
        User.objects.create(username=username, password=hashed_password, email=email)

        return JsonResponse({'message': '注册成功'})
    except KeyError:
        return HttpResponseBadRequest('Invalid data')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return JsonResponse({
                    'message': '登录成功',
                    'access': access_token,
                    'refresh': str(refresh)
                })
            else:
                return JsonResponse({'error': 'Invalid password'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)
    except KeyError:
        return HttpResponseBadRequest('Invalid data')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')


@require_http_methods(["GET"])
def get_user_all(request):
    # 获取所有 User 对象
    users = User.objects.all()

    # 创建一个列表来存储用户数据
    user_list = []
    for user in users:
        user_data = {
            'username': user.username,
            'email': user.email,
            'register_date': user.register_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
        user_list.append(user_data)

    # 返回 JSON 响应
    return JsonResponse(user_list, safe=False)

