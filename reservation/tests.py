from datetime import timedelta, date
from time import sleep

from django.conf import settings

from accounts.models import Transaction
from django.contrib.auth.models import User
from django.test import override_settings, tag
from habitats.models import Habitat, RoomType
from reservation.models import Reservation
from users.models import Member
from utils.test import SeleniumTestCase


@tag('ui')
class TestReservation(SeleniumTestCase):

    def setUp(self):
        super().setUp()

        self.cost_per_day = 100000

        self.user = User.objects.create_user('ali', None, 'hello')
        self.habitat_owner_user = User.objects.create_user('owner', None, 'hello')
        self.member = Member.objects.create(user=self.user)
        self.owner_member = Member.objects.create(user=self.habitat_owner_user)
        self.habitat = Habitat.objects.create(name='hello', owner=self.owner_member)
        self.room = RoomType.objects.create(
            habitat=self.habitat,
            number_of_rooms_of_this_kind=2,
            cost_per_night=self.cost_per_day,
        )

        self.selenium_client.login('ali', 'hello')

    @override_settings(DEBUG=True)
    def test_reserve_success(self):
        Transaction.objects.create(from_user=None, to_user=self.user, amount=10000000, verified=True)
        self.selenium_client.get('/reservation/{}/?from_date={}&to_date={}'.format(
            self.habitat.id,
            date.today() + timedelta(days=50),
            date.today() + timedelta(days=52),
        ))
        button = self.selenium_client.web_driver.find_elements_by_tag_name('input')[-1]
        button.location_once_scrolled_into_view
        button.click()
        sleep(1)
        button = self.selenium_client.web_driver.find_elements_by_tag_name('a')[-1]
        button.location_once_scrolled_into_view
        button.click()
        sleep(1)
        self.assertEqual(Transaction.get_balance_from_user(self.user), 10000000 - self.cost_per_day * 2)

    def get_cancel_buttons(self):
        return self.selenium_client.web_driver.find_elements_by_tag_name(
            'table'
        )[0].find_elements_by_tag_name('button')

    @override_settings(DEBUG=True)
    def test_cancellation(self):
        Transaction.objects.create(from_user=None, to_user=self.user, amount=10000000, verified=True)
        today = date.today()
        for date_pair in (
                (today - timedelta(days=1), today),
                (today + timedelta(days=5), today + timedelta(days=7)),
                (today + timedelta(days=10), today + timedelta(days=12)),
                (today + timedelta(days=15), today + timedelta(days=17)),
        ):
            self.selenium_client.get('/reservation/{}/?from_date={}&to_date={}'.format(
                self.habitat.id,
                *date_pair
            ))
            button = self.selenium_client.web_driver.find_elements_by_tag_name('input')[-1]
            button.location_once_scrolled_into_view
            button.click()
            sleep(1)
            button = self.selenium_client.web_driver.find_elements_by_tag_name('a')[-1]
            button.location_once_scrolled_into_view
            button.click()
            sleep(1)
        self.assertEqual(Transaction.get_balance_from_user(self.user), 10000000 - self.cost_per_day * 6)

        # do a little stupid thing to travel in the time
        for reservation in Reservation.objects.all():
            reservation.from_date -= timedelta(days=5)
            reservation.to_date -= timedelta(days=5)
            reservation.save()

        self.selenium_client.get('/reservation/list')

        cancel_buttons = self.get_cancel_buttons()
        self.assertEqual(len(cancel_buttons), 2)

        cancel_buttons[0].click()
        sleep(1)

        cancel_buttons = self.get_cancel_buttons()
        self.assertEqual(len(cancel_buttons), 1)

        cancel_buttons[0].click()
        sleep(1)

        cancel_buttons = self.get_cancel_buttons()
        self.assertEqual(len(cancel_buttons), 0)

        punishment = self.cost_per_day * 2 * settings.CANCELLATION_FEE * 5
        self.assertEqual(
            Transaction.get_balance_from_user(self.user),
            10000000 - self.cost_per_day * 2 - punishment
        )

        self.assertEqual(
            Transaction.get_balance_from_user(self.habitat_owner_user),
            self.cost_per_day * 2 * (1 - settings.RESERVATION_FEE) + punishment
        )

    @override_settings(DEBUG=True)
    def test_reserve_failure(self):
        self.selenium_client.get('/reservation/{}/?from_date=2019-07-07&to_date=2019-07-08'.format(self.habitat.id))
        button = self.selenium_client.web_driver.find_elements_by_tag_name('input')[-1]
        button.location_once_scrolled_into_view
        button.click()
        sleep(1)
        button = self.selenium_client.web_driver.find_elements_by_tag_name('a')[-1]
        button.location_once_scrolled_into_view
        button.click()
        sleep(1)
        self.assertIn('امروز', self.selenium_client.web_driver.page_source)

        self.selenium_client.get('/reservation/{}/?from_date={}&to_date={}'.format(
            self.habitat.id,
            date.today() + timedelta(days=50),
            date.today() + timedelta(days=52),
        ))
        button = self.selenium_client.web_driver.find_elements_by_tag_name('input')[-1]
        button.location_once_scrolled_into_view
        button.click()
        sleep(1)
        button = self.selenium_client.web_driver.find_elements_by_tag_name('a')[-1]
        button.location_once_scrolled_into_view
        button.click()
        sleep(1)
        self.assertIn('شارژ', self.selenium_client.web_driver.page_source)
