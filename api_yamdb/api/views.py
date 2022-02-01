from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from rest_framework.decorators import api_view

from .serializers import SignUpSerializer
from .tokens import account_activation_token


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            mail_subject = 'Подтверждение Вашего e-mail. YamDb.'
            token = account_activation_token.make_token(user)
            message = (
                    'Для завершения регистрации подтвердите Ваш email.' +
                    f'\n Token:{token}'
            )
            to_email = serializer.initial_data['email']
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Пожалуйста, проследуйте инструкциям на email')








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
