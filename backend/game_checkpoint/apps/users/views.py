from cgitb import lookup
import json
from django.conf import settings
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .serializers import CookieTokenRefreshSerializer, ProfileSerializer, UserRegisterSerializer, FollowSerializer, SessionSerializer
from .backends import CookieJWTAuthentication
from .models import User
from urllib.parse import quote

class CookieTokenObtainPairView(TokenObtainPairView):
    permission_classes = (~IsAuthenticated,)
    authentication_classes = (CookieJWTAuthentication,)

    def finalize_response(self, request, response, *args, **kwargs):

        cookie_max_age = 3600 * 24 * 14  # 14 days

        if response.data.get('access'):

            user = User.objects.get(email=request.data['email'])
            serializer = SessionSerializer(user)
            response.set_cookie(
                'gcuser', quote(json.dumps(serializer.data)), max_age=cookie_max_age
            )
            response.set_cookie(
                settings.JWT_AUTH['JWT_AUTH_COOKIE'], response.data['access'], max_age=cookie_max_age, httponly=True)

        if response.data.get('refresh'):
            response.set_cookie(settings.JWT_AUTH['JWT_REFRESH_COOKIE'],
                                response.data['refresh'], max_age=cookie_max_age, httponly=True)
            del response.data['refresh']

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CookieJWTAuthentication,)
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        

        cookie_max_age = 3600 * 24 * 14  # 14 days

        if response.data.get('access'):
            user = User.objects.get(email=request.user.email)
            serializer = SessionSerializer(user)
            response.set_cookie(
                'gcuser', quote(json.dumps(serializer.data)), max_age=cookie_max_age
            )
            response.set_cookie(
                settings.JWT_AUTH['JWT_AUTH_COOKIE'], response.data['access'], max_age=cookie_max_age, httponly=True)

        if response.data.get('refresh'):
            response.set_cookie(settings.JWT_AUTH['JWT_REFRESH_COOKIE'],
                                response.data['refresh'], max_age=cookie_max_age, httponly=True)
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)


class RegisterViewSet(mixins.CreateModelMixin, GenericViewSet):
    # must NOT (~) be authenticated
    permission_classes = (~IsAuthenticated,)
    serializer_class = UserRegisterSerializer


class LogoutView(views.APIView):

    def post(self, request, *args, **kwargs):
        response = Response({'ok': True})
        response.delete_cookie(settings.JWT_AUTH['JWT_AUTH_COOKIE'])
        response.delete_cookie(settings.JWT_AUTH['JWT_REFRESH_COOKIE'])
        response.delete_cookie('gcuser')
        return response

class ProfileView(mixins.RetrieveModelMixin, GenericViewSet):
    permissions_classes = (IsAuthenticated)
    serializer_class = ProfileSerializer
    lookup_field = 'username'
    queryset = User.objects.all()

    def details(self, request, *args, **kwargs):
        follow = self.get_object()
        serializer_context = {
            'user': request.user,
            'follow': follow
        }
        serializer = self.serializer_class(
            follow,
            context=serializer_context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

class FollowView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer
    lookup_field = 'username'
    queryset = User.objects.all()

    def follow(self, request, *args, **kwargs):
        follow = self.get_object()
        serializer_context = {
            'user': request.user,
            'follow': follow
        }
        serializer = self.serializer_class(
            follow,
            context=serializer_context
        )
        serializer.create()
        return Response({'mgs': 'Successfuly create'}, status=status.HTTP_200_OK)

    def unfollow(self, request, *args, **kwargs):
        follow = self.get_object()
        serializer_context = {
            'user': request.user,
            'follow': follow
        }
        serializer = self.serializer_class(
            follow,
            context=serializer_context
        )
        serializer.delete()
        return Response({'mgs': 'Successfuly create'}, status=status.HTTP_200_OK)