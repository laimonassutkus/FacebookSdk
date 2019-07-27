from typing import Optional
from django.conf import settings


class WallPostService:
    __instance = None

    def __new__(cls):
        if WallPostService.__instance is None:
            WallPostService.__instance = object.__new__(cls)

            cls.__access_token = settings.FACEBOOK_ACCESS_TOKEN
            cls.__application_id = settings.FB_APP_ID

        return WallPostService.__instance

    def post(
            self,
            full_picture: Optional[str] = None,
            caption: Optional[str] = None,
            description: Optional[str] = None,
            message: Optional[str] = None
    ) -> None:
        kwargs = {
            'full_picture': full_picture,
            'caption': caption,
            'description': description,
            'message': message
        }

        # Filter any None parameters.
        kwargs = {key: value for key, value in kwargs.items() if value}

        # Post to facebook wall.
        raise NotImplementedError('This feature is not supported yet.')
