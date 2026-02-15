from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
try:
    from django_ratelimit.decorators import ratelimit
    from django.utils.decorators import method_decorator
    RATELIMIT_AVAILABLE = True
except ImportError:
    RATELIMIT_AVAILABLE = False
    def ratelimit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    method_decorator = lambda x: lambda y: y
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer
from .permissions import IsAdmin, IsStudentOrAdmin

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    def get_permissions(self):
        if self.action in ['create', 'register']:
            return [permissions.AllowAny()]
        elif self.action in ['destroy', 'update', 'partial_update']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny],
           authentication_classes=[])
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST'))
    def register(self, request):
        """User registration endpoint"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """Logout endpoint - blacklist refresh token"""
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def verify_email(self, request):
        """Mock email verification endpoint"""
        user = request.user
        user.is_email_verified = True
        user.save()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def delete_account(self, request):
        """GDPR-style account deletion"""
        user = request.user
        user.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@ratelimit(key='ip', rate='5/m', method='POST')
@authentication_classes([])
def login(request):
    """JWT Login endpoint - accepts email or username"""
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    
    data = request.data.copy()
    
    # If email is provided instead of username, look up the username
    email = data.get('email')
    if email and not data.get('username'):
        try:
            user = User.objects.get(email=email)
            data['username'] = user.username
        except User.DoesNotExist:
            return Response(
                {'detail': 'No account found with this email.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    serializer = TokenObtainPairSerializer(data=data)
    if serializer.is_valid():
        user = serializer.user
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(serializer.validated_data['refresh']),
            'access': str(serializer.validated_data['access']),
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
