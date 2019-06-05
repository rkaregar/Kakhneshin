from time import sleep

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, tag, LiveServerTestCase
from django.test import override_settings
from habitats.models import Habitat
from users.models import Member
from utils.test import KakhneshinCRUDTestCase, SeleniumDjangoTestClient


class HabitatsCRUDTest(KakhneshinCRUDTestCase):

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


@tag('backend')
class HabitatsBackendTest(HabitatsCRUDTest, TestCase):

    def setUp(self):
        super().setUp()
        test_user = User.objects.create_user('test', 'test@kakhneshin.ir', password='test')
        self.client.force_login(test_user)


@tag('ui')
@override_settings(**settings.TEST_SETTINGS)
class HabitatSeleniumTest(HabitatsCRUDTest, LiveServerTestCase):

        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            cls.selenium_client = SeleniumDjangoTestClient(
                live_server_url=cls.live_server_url
            )

        def setUp(self):
            super().setUp()
            self.client = self.selenium_client
            Member.objects.create(user=User.objects.create_user('test', 'test@kakhneshin.ir', password='test'))
            self.client.post('/users/login/', data={'username': 'test', 'password': 'test'})

        @classmethod
        def tearDownClass(cls):
            cls.selenium_client.web_driver.close()
            super().tearDownClass()









