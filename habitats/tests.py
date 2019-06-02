from django.conf import settings
from django.contrib.auth.models import User
from django.test import LiveServerTestCase, override_settings
from django.test import TestCase
from habitats.models import Habitat
from selenium import webdriver

# Create your tests here.
from utils.test import KakhneshinCRUDTestCase, SeleniumDjangoTestClient


class HabitatsBackendTest(KakhneshinCRUDTestCase, TestCase):

    read_url = '/habitats/{}/update/'
    list_url = '/habitats/'
    create_url = '/habitats/create/'
    update_url = '/habitats/{}/update/'
    delete_url = '/habitats/{}/delete/'

    model = Habitat
    model_test_data = [
        {
            'name': 'اقامتگاه اول',
            'address': 'اول آنجایی که می‌دانی',
            'town': 'تهران',
            'cost': 100000,
        },
        {
            'name': 'دومین اقامتگاه اول',
            'address': 'اول آنجایی که می‌دانی',
            'town': 'تهران',
            'cost': 100000,
        }
    ]
    visible_fields = ('name', 'address', 'town', 'cost')

    def setUp(self):
        super().setUp()
        test_user = User.objects.create_user('test', 'test@kakhneshin.ir', password='test')
        self.client.force_login(test_user)

@override_settings(**settings.TEST_SETTINGS)
class HabitatSeleniumTest(HabitatsBackendTest, LiveServerTestCase):


        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            cls.selenium_client = SeleniumDjangoTestClient(
                web_driver=webdriver.Firefox(),
                live_server_url=cls.live_server_url
            )

        def setUp(self):
            super().setUp()
            self.client = self.selenium_client





