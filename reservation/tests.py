from time import sleep

from accounts.models import Transaction
from django.contrib.auth.models import User
from django.test import override_settings
from habitats.models import Habitat, RoomType
from selenium import webdriver
from users.models import Member
from utils.test import SeleniumTestCase


class TestReservation(SeleniumTestCase):

    def setUp(self):
        super().setUp()

        self.cost_per_day = 100000

        self.user = User.objects.create_user('ali', None, 'hello')
        self.member = Member.objects.create(user=self.user)
        self.habitat = Habitat.objects.create(name='hello', owner=self.member)
        self.room = RoomType.objects.create(
            habitat=self.habitat,
            number_of_rooms_of_this_kind=2,
            cost_per_night=self.cost_per_day,
        )

        self.selenium_client.login('ali', 'hello')


    @override_settings(DEBUG=True)
    def test_reserve_success(self):
        Transaction.objects.create(from_user=None, to_user=self.user, amount=10000000, verified=True)
        self.selenium_client.get('/reservation/{}/?from_date=2019-07-07&to_date=2019-07-07'.format(self.habitat.id))
        sleep(10)
        button = self.selenium_client.web_driver.find_elements_by_tag_name('input')[-1]
        button.location_once_scrolled_into_view
        sleep(10)
        button.click()
        sleep(100)
        self.assertEqual(Transaction.get_balance_from_user(self.user), 10000000 - self.cost_per_day)


    # @override_settings(DEBUG=True)
    # def test_reserve_failure(self):
    #     self.selenium_client.get('/reservation/{}/?from_date=2019-07-07&to_date=2019-07-07'.format(self.habitat.id))
    #     button = self.selenium_client.web_driver.find_elements_by_tag_name('input')[-1]
    #     button.location_once_scrolled_into_view
    #     button.click()
    #     self.assertIn('شارژ', self.selenium_client.web_driver.page_source)
    #
    #
    #
