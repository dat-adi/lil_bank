from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from logging import getLogger, DEBUG

UserModel = get_user_model()


class BaseUserTest(TestCase):
    USERNAME = None
    PASSWORD = None
    USER_EMAIL = None
    logger = None

    @classmethod
    def setUpTestData(cls):
        cls.logger = getLogger(__name__)
        cls.logger.setLevel(level=DEBUG)

        cls.USERNAME: str = "test_user_1"
        cls.PASSWORD: str = "test_user_password"
        cls.USER_EMAIL: str = "test@user.com"

        cls.client = Client(enforce_csrf_checks=False)

        try:
            cls.user_model = UserModel.objects.get(username=cls.USERNAME)
        except ObjectDoesNotExist:
            cls.user_model = UserModel.objects.create_user(
                username=cls.USERNAME,
                password=cls.PASSWORD,
                email=cls.USER_EMAIL
            )

    @classmethod
    def login_client(cls):
        cls.logger.info("Logging in the client")
        cls.client.login(
            username=cls.USERNAME,
            password=cls.PASSWORD
        )

    @classmethod
    def logout_client(cls):
        cls.logger.info("Logging out the client")
        cls.client.logout()
