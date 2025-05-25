from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework import status  # 🔁 status.HTTP_400_BAD_REQUEST용

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
    
    from products.models import DepositProduct  # 지연 import: 순환 참조 방지

    try:
        product = DepositProduct.objects.get(fin_prdt_cd=product_id)
        request.user.joined_products.add(product)  # ManyToManyField에 추가
        return Response({'message': '가입이 완료되었습니다.'})
    except DepositProduct.DoesNotExist:
        return Response({'error': '해당 상품을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
