from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import NotYourProfileError, ProfileDoesNotExist
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer


class AgentListAPIView(generics.ListAPIView):
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        agents = Profile.objects.filter(is_agent=True)
        serializer = self.serializer_class(agents, many=True)
        return Response(serializer.data)


"""
# Function-based view
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def agent_list_api_view(request):
    agents = Profile.objects.filter(is_agent=True)
    serializer = ProfileSerializer(agents, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
"""


class TopAgentsListAPIView(generics.ListAPIView):
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        agents = Profile.objects.filter(top_agent=True)
        serializer = self.serializer_class(agents, many=True)
        return Response(serializer.data)


class GetProfileAPIView(APIView):
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    # def get(self, request, format=None):
    #     serializer = self.serializer_class(
    #         instance=request.user.profile, context={"request": request}
    #     )
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data)


class ProfileUpdateAPIView(APIView):
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    # def put(self, request, format=None):
    #     serializer = self.serializer_class(
    #         request.user.profile, data=request.data, partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, username):
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist("Profile does not exist")

        user_name = request.user.username
        if user_name != username:
            raise NotYourProfileError("Not your profile to update")

        serializer = self.serializer_class(
            instance=request.user.profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
