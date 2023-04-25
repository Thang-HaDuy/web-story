from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response
from rest_framework import generics, viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer, UserCurrentSerializer

from story.serializers import StoryTopSerializer
from action.serializers import (
    RatingSerializer,
    LikeSerializer,
    CommentSerializer,
    ViewSerializer,
    FollowSerializer,
)

token_generator = PasswordResetTokenGenerator()


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['get_current_user', 'change_password', 'get_comment', 'get_rating', 'change-avatar']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=True, url_path='history-story')
    def get_history_story(self, request, pk):
        view = self.get_object().view.all().distinct("story").order_by('-story', '-created_date')

        return Response(ViewSerializer(view, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(self, request):
        return Response(UserCurrentSerializer(request.user, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='story')
    def get_story(self, request, pk):
        story = self.get_object().story.filter(active=True).order_by('-created_date')

        return Response(StoryTopSerializer(story, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='follow')
    def get_follow(self, request, pk):
        story = self.get_object().follow.filter(active=True).order_by('-created_date')

        return Response(FollowSerializer(story, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='comment')
    def get_comment(self, request, pk):
        comment = self.get_object().comment.filter(active=True).order_by('-created_date')

        return Response(CommentSerializer(comment, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='rating')
    def get_rating(self, request, pk):
        rating = self.get_object().rating.filter(active=True)

        return Response(RatingSerializer(rating, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=False, url_path='change-password')
    def change_password(self, request):
        user = request.user

        if user.check_password(request.data.get('old_password')):
            user.set_password(request.data.get('new_password'))
            user.save()

            return Response(status=status.HTTP_200_OK)

        return Response({"old password": ['wrong password.']}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['patch'], detail=False, url_path='change-avatar')
    def change_avatar(self, request):
        user = request.user
        avatar = request.data.get('avatar')

        if avatar is not None and user is not None:
            user.avatar = avatar
            user.save()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)



@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    if created:
        try:
            subject = 'Activate Your Account'
            email_from = settings.EMAIL_HOST_USER
            to_email = instance.email
            message = render_to_string(
                'user/activate_account.html',
                {
                    'user': instance,
                    'domain': settings.DOMAIN_URL,
                    'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                    'token': token_generator.make_token(instance),
                }
            )
            send_mail(subject,
                      message,
                      email_from,
                      [to_email])
        except Exception as error:
            print(error)



class ActiveEmail(APIView):
    def post(self, request):
        try:
            uidb64 = request.data.get('uidb64')
            token = request.data.get('token')
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Http404:
            user = None
        if user is not None and token_generator.check_token(user, token):
            user.is_email = True
            user.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ForgotPassword(APIView):
    def post(self, request):
        author = User.objects.get(email=request.data.get('email'))

        if author is not None:
            try:
                subject = 'Forgot Your Account'
                email_from = settings.EMAIL_HOST_USER
                to_email = author.email
                message = render_to_string(
                    'user/reset_password.html',
                    {
                        'user': author,
                        'domain': settings.DOMAIN_URL,
                        'uid': urlsafe_base64_encode(force_bytes(author.pk)),
                        'token': token_generator.make_token(author),
                    }
                )
                send_mail(subject,
                          message,
                          email_from,
                          [to_email])
                return Response(status=status.HTTP_200_OK)
            except Exception as error:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    def patch(self, request):
        try:
            uidb64 = request.data.get('uidb64')
            token = request.data.get('token')
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Http404:
            user = None
        if user is not None and token_generator.check_token(user, token):
            user.set_password(request.data.get('password'))
            user.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class OAuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)

# Create your views here.
