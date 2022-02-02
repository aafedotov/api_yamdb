from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView

from .serializers import SignUpSerializer, GetTokenSerializer
from users.models import CustomUser


@api_view(['POST'])
def signup(request):
    """Регистрация пользователей."""
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            mail_subject = 'Email confirmation. YamDb.'
            token = default_token_generator.make_token(user)
            message = (
                    'Для завершения регистрации подтвердите Ваш email.' +
                    f'\nToken:{token}'
            )
            to_email = serializer.initial_data['email']
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return Response('Пожалуйста, проследуйте инструкциям на email')
        else:
            print(serializer.errors)
            if 'exists' in str(serializer.errors['username']):
                user = CustomUser.objects.get(username=request.data['username'])
                if request.data['email'] != user.email:
                    return Response('Указан неверный email пользователя')
                mail_subject = 'Email confirmation. YamDb.'
                token = default_token_generator.make_token(user)
                message = (
                        'Для завершения регистрации подтвердите Ваш email.' +
                        f'\nToken:{token}'
                )
                to_email = serializer.initial_data['email']
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return Response('Пожалуйста, проследуйте инструкциям на email')
        return Response('Невалидный запрос к API.')


class GetTokenApiView(APIView):
    """Получение JWT токена."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = GetTokenSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            if CustomUser.objects.filter(username=username).exists():
                user = CustomUser.objects.get(username=username)
                if default_token_generator.check_token(user, confirmation_code):
                    access_token = RefreshToken.for_user(user).access_token
                    data = {"token": str(access_token)}
                    return Response(data, status=status.HTTP_201_CREATED)
            return Response('Пользователь не найден', status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# from rest_framework.response import Response
# from rest_framework import generics, status
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.sites.shortcuts import get_current_site
#
# from api_yamdb.users.models import CustomUser
# from .utils import Util
#
#
# class RegisterView(generics.GenericAPIView):
#     """View-класс для регистрации пользователей."""
#
#     serializer_class = RegisterSerializer
#
#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data
#
#         user = CustomUser.objects.get(email=user_data['email'])
#         token = RefreshToken.for_user(user)
#         current_site = get_current_site(request)
#
#         data = {
#             'domain': current_site.domain
#         }
#         Util.send_email(data)
#
#         return Response(user_data, status=status.HTTP_201_CREATED)
#
#
