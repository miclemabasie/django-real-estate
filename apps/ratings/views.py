from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.profiles.models import Profile

from .models import Rating

User = get_user_model()


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_agent_review(request, profile_id):
    """
    Create a review for an agent
    """
    try:
        agent_profile = Profile.objects.get(id=profile_id, is_agent=True)
    except Profile.DoesNotExist:
        formatted_response = {
            "error": "The agent you are trying to review does not exist",
        }
        return Response(formatted_response, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    profile_user = User.objects.get(pkid=agent_profile.user.pkid)

    if profile_user.email == request.user.email:
        formatted_response = {
            "error": "You cannot rate yourself",
        }
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

    alreadyExists = agent_profile.agent_reviews.filter(
        agent__pkid=profile_user.pkid
    ).exists()
    if alreadyExists:
        formatted_response = {
            "error": "You have already reviewed this agent",
        }
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

    elif data["rating"] == 0:
        formatted_response = {
            "error": "Please select a rating",
        }
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
    else:
        review = Rating.objects.create(
            rater=request.user,
            agent=agent_profile,
            rating=data["rating"],
            comment=data["comment"],
        )
        reviews = agent_profile.agent_reviews.all()
        agent_profile.num_reviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        return Response(
            {"success": "You have successfully reviewed this agent"},
            status=status.HTTP_201_CREATED,
        )
