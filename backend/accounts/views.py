from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework import status  # 🔁 status.HTTP_400_BAD_REQUEST용
from products.models import DepositProduct


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
    if not product_id:
        return Response({'error': '상품 ID가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ 현재 가입한 상품 수가 5개 이상이면 거부
    if request.user.joined_products.count() >= 5:
        return Response({'error': '가입 가능한 최대 상품 수(5개)를 초과했습니다.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        product = DepositProduct.objects.get(fin_prdt_cd=product_id)
    except DepositProduct.DoesNotExist:
        return Response({'error': '해당 상품을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # 이미 가입한 경우 중복 방지
    if request.user.joined_products.filter(fin_prdt_cd=product_id).exists():
        return Response({'message': '이미 가입한 상품입니다.'})

    request.user.joined_products.add(product)
    return Response({'message': '가입이 완료되었습니다.'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def leave_product(request):
    product_id = request.data.get('product_id')

    if not product_id:
        return Response({'error': '상품 ID가 필요합니다.'}, status=400)

    try:
        product = DepositProduct.objects.get(fin_prdt_cd=product_id)
    except DepositProduct.DoesNotExist:
        return Response({'error': '해당 상품이 존재하지 않습니다.'}, status=404)

    request.user.joined_products.remove(product)
    return Response({'message': '가입 취소 완료'})
