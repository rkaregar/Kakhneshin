from time import sleep

from django.contrib.auth.models import User
from django.test import LiveServerTestCase, override_settings
from habitats.models import Habitat, RoomType
from selenium import webdriver
from users.models import Member


class TestReservation(LiveServerTestCase):

    def setUp(self):
        super().setUp()
        self.web_driver = webdriver.Firefox()

        self.user = User.objects.create_user('ali')
        self.member = Member.objects.create(user=self.user)
        self.habitat = Habitat.objects.create(name='hello', owner=self.member)


    @override_settings(DEBUG=True)
    def test_reserve(self):
        self.web_driver.get(self.live_server_url + '/reservation/search?daterange=07/07/2019 - 07/07/2019')
        sleep(10)

    def tearDown(self):
        self.web_driver.close()
        super().tearDown()


