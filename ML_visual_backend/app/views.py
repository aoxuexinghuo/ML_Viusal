import json

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from .algs.linear_regression import linear_regression
from .jwt_utils import create_access_token, decode_access_token, validate_token
from .models import User


@swagger_auto_schema(
    operation_summary="注册",
    tags=['用户接口'],
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='邮箱'),
        }),
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='注册成功'),
        }
    )}
)
@csrf_exempt
@require_http_methods(["POST"])
@api_view(['POST'])
def register(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        email = data['email']

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': '用户名已存在'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': '邮箱已存在'}, status=400)

        hashed_password = make_password(password)
        User.objects.create(username=username, password=hashed_password, email=email)

        return JsonResponse({'message': '注册成功'})
    except KeyError:
        return HttpResponseBadRequest('Invalid data')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')


@swagger_auto_schema(
    operation_summary="登录",
    tags=['用户接口'],
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
        }),
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='登录成功'),
            'access': openapi.Schema(type=openapi.TYPE_STRING, description='access token'),
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='refresh token'),
        }
    )})
@csrf_exempt
@require_http_methods(["POST"])
@api_view(['POST'])
def login(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            return JsonResponse({'error': '用户不存在'}, status=400)

        if not check_password(password, user.password):
            return JsonResponse({'error': '密码错误'}, status=400)

        access_token = create_access_token(identity=user.username)

        return JsonResponse({'message': '登录成功', 'access': access_token})
    except KeyError:
        return HttpResponseBadRequest('Invalid data')
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')


@swagger_auto_schema(
    operation_summary="获取用户信息",
    tags=['用户接口'],
    methods=['GET'],
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='邮箱'),
            'register_date': openapi.Schema(type=openapi.TYPE_STRING, description='注册时间'),
        }
    )})
@require_http_methods(["GET"])
@api_view(['GET'])
def get_user_info(request):
    try:
        username = validate_token(request)
        if username is None:
            return JsonResponse({'error': '未登录'}, status=401)

        user = User.objects.filter(username=username).first()
        if user is None:
            return JsonResponse({'error': '用户不存在'}, status=404)

        return JsonResponse({
            'username': user.username,
            'email': user.email,
            'register_date': user.register_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return JsonResponse({'error': '请求失败'}, status=500)


@swagger_auto_schema(
    operation_summary="线性回归",
    tags=['算法接口'],
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'inputData': openapi.Schema(type=openapi.TYPE_ARRAY, description='输入数据', items=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_NUMBER))),
        }),
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'predictData': openapi.Schema(type=openapi.TYPE_ARRAY, description='预测数据', items=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_NUMBER))),
        }
    )})
@csrf_exempt
@require_http_methods(["POST"])
@api_view(['POST'])
def linear_regression_api(request):

    data = json.loads(request.body)

    input = data['inputData']

    result = linear_regression(input)

    return JsonResponse({
        'predictData': result,
    })

