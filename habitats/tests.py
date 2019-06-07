from time import sleep

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.test import override_settings
from habitats.models import Habitat
from users.models import Member
from utils.test import KakhneshinCRUDTestCase, create_user, SeleniumTestCase


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
        },
        {
            'name': 'دومین اقامتگاه اول',
            'address': 'اول آنجایی که می‌دانی',
            'town': 'تهران',
        }
    ]
    visible_fields = ('name', 'address', 'town')


@tag('backend')
class HabitatsBackendTest(HabitatsCRUDTest, TestCase):

    def setUp(self):
        super().setUp()
        test_user = User.objects.create_user('test', 'test@kakhneshin.ir', password='test')
        self.client.force_login(test_user)


@tag('ui')
@override_settings(**settings.TEST_SETTINGS)
class HabitatSeleniumTest(HabitatsCRUDTest, SeleniumTestCase):


        def setUp(self):
            super().setUp()
            self.client = self.selenium_client
            test_user = create_user(username='test', password='test')
            self.client.login(username=test_user.username, password='test')










