from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework import status  # 🔁 status.HTTP_400_BAD_REQUEST용
from products.models import DepositProduct
from .models import JoinedProduct, InterestOption 



User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_page(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_password(request):
    password = request.data.get('password')
    if password and request.user.check_password(password):
        return Response({'success': True})
    return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': '사용자를 찾을 수 없습니다.'}, status=404)
    
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_product(request):
    product_id = request.data.get('product_id')
    option_id = request.data.get('option_id')

    if not product_id or not option_id:
        return Response({'error': '상품 ID와 옵션 ID가 필요합니다.'}, status=400)

    if request.user.joinedproduct_set.count() >= 5:
        return Response({'error': '최대 5개까지만 가입 가능합니다.'}, status=403)

    try:
        product = DepositProduct.objects.get(fin_prdt_cd=product_id)
        option = InterestOption.objects.get(id=option_id, product=product)
    except (DepositProduct.DoesNotExist, InterestOption.DoesNotExist):
        return Response({'error': '상품 또는 옵션을 찾을 수 없습니다.'}, status=404)

    # 중복 가입 방지
    if JoinedProduct.objects.filter(user=request.user, option=option).exists():
        return Response({'message': '이미 해당 조건으로 가입한 상품입니다.'})

    JoinedProduct.objects.create(user=request.user, product=product, option=option)
    return Response({'message': '가입 완료'})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def leave_product(request):
    option_id = request.data.get('option_id')

    try:
        joined = JoinedProduct.objects.get(user=request.user, option_id=option_id)
        joined.delete()
        return Response({'message': '가입 취소 완료'})
    except JoinedProduct.DoesNotExist:
        return Response({'error': '가입 내역이 없습니다.'}, status=404)
    
    
@api_view(['GET'])
def check_username(request):
    username = request.query_params.get('username', '')
    exists = User.objects.filter(username=username).exists()
    return Response({'available': not exists})

