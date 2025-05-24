from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework import status  # 🔁 status.HTTP_400_BAD_REQUEST용


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
