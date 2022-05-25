from django.http import JsonResponse
from inaequo_server import response_codes
import json


def signup(request):
    if request.method is "POST":
        data = json.loads(request.body)

        # Validating data
        user_id = data.get("user-id", None)  # User id can be either email address or username
        password = data.get("password", None)  # User password
        if not password or not user_id:
            return JsonResponse({
                "response-code": response_codes.INVALID_KEY,
            })

        # Authenticating user
        # todo: Choose authentication scheme and log in the user
        user = {
            "id": 1,
            "full_name": "Test User",
        }

        return JsonResponse({
            "registration-id": user.get("id", None),
            "user-name": user.get("full_name", None),
            "response-code": response_codes.SUCCESSFUL,
        })
