# Import pytest and your factories
import pytest
from tests.factories import UserFactory, ProfileFactory


# # Define your test function
# def test_profile_str(profile_instance):
#     print("#######################", profile_instance.user.first_name)
#     assert profile_instance.__str__() == f"{profile_instance.user.username}'s Profile"
