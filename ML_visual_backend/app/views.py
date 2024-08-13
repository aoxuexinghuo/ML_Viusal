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
from .algs.decision_tree_id3 import decision_tree_id3
from .algs.decision_tree_id3 import generate_tree_mermaid_code
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


@swagger_auto_schema(
    operation_summary="决策树(ID3)",
    tags=['算法接口'],
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,  # 请求体是一个对象
        properties={
            'inputData': openapi.Schema(
                type=openapi.TYPE_ARRAY,  # 'inputData' 是一个数组
                description='输入数据',  # 描述 'inputData' 为输入数据
                items=openapi.Schema(
                    type=openapi.TYPE_ARRAY,  # 数组中的每个元素也是一个数组
                    items=openapi.Schema(type=openapi.TYPE_STRING)  # 数组中的每个元素是字符串类型
                )
            ),
            'featureName': openapi.Schema(
                type=openapi.TYPE_ARRAY,  # 'featureName' 是一个数组
                description='特征名称',  # 描述 'featureName' 为特征名称
                items=openapi.Schema(type=openapi.TYPE_STRING)  # 数组中的每个元素是字符串类型
            )
        }
    ),
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,  # 响应体是一个对象
        properties={
            'ID3_tree': openapi.Schema(
                type=openapi.TYPE_OBJECT,  # 'ID3_tree' 是一个对象
                description='决策树(ID3)的mermaid代码',  # 描述 'ID3_tree' 为决策树
                additional_properties=openapi.Schema(type=openapi.TYPE_OBJECT)  # 对象可以包含任意属性
            ),
        }
    )}
)
@csrf_exempt  # 禁用 CSRF 保护，通常用于 API 接口
@require_http_methods(["POST"])  # 限制视图函数只接受 POST 请求
@api_view(['POST'])  # 将视图函数标记为 Django REST framework 的视图函数，接受 POST 请求
def decision_tree_id3_api(request):
    # 从请求的主体中加载 JSON 数据
    data = json.loads(request.body)

    # 提取 'inputData' 属性
    input_data = data['inputData']
    feature_name = data['featureName']
    # 将数据转换为字典格式
    data_dicts = [dict(zip(feature_name, row)) for row in input_data]
    # 调用决策树函数，传入输入数据，并获取决策树结果
    result_tree_mermaid_code = generate_tree_mermaid_code(data_dicts)
    # 返回 JSON 响应，其中包含决策树的mermaid代码
    return JsonResponse({
        'ID3_tree_mermaid_code': result_tree_mermaid_code,  # 'ID3_tree' 是生成的决策树
    })
