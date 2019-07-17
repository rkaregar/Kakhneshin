from urllib.parse import urlencode

from accounts.models import Transaction
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, tag, LiveServerTestCase, override_settings
from utils.test import create_user, SeleniumTestCase, SeleniumResponse
from unittest import skip


class SetupUserAndAccountMixin:

    def setUp(self):
        super().setUp()
        self.user = create_user()
        self.staff_user = create_user(username='staff', is_staff=True)
        self.prior_balance = 12143
        Transaction.objects.create(to_user=self.user, amount=self.prior_balance, verified=True)


class DepositTest(SetupUserAndAccountMixin):

    def test_deposit(self):
        self.client.force_login(self.user)
        post_url = self.navigate_to_deposit_page()
        amount = 1452
        response = self.client.post(post_url, data={'amount': amount}, follow=True)
        self.assertTrue('تایید پرداخت' in response.content.decode('utf8'))
        response = self.confirm_payment()
        self.assertTrue('شارژ حساب با موفقیت انجام شد.' in response.content.decode('utf8'))
        self.assertTrue(str(amount + self.prior_balance) in response.content.decode('utf8'))

    def test_deposit_error(self):
        self.client.force_login(self.user)
        post_url = self.navigate_to_deposit_page()
        amount = 1452
        response = self.client.post(post_url, data={'amount': amount}, follow=True)
        self.assertTrue('لغو پرداخت' in response.content.decode('utf8'))
        response = self.reject_payment()
        self.assertTrue('پرداخت توسط کاربر لغو شد' in response.content.decode('utf8'))
        self.assertTrue(str(self.prior_balance) in response.content.decode('utf8'))


    def navigate_to_deposit_page(self):
        response = self.client.get('/accounts/deposit/')
        self.assertEqual(response.status_code, 200)
        return '/accounts/deposit/'

    def confirm_payment(self):
        return self.client.get('/accounts/callback/{}/?status=OK'.format(
            Transaction.objects.order_by('id').last().token
        ))

    def reject_payment(self):
        return self.client.get('/accounts/callback/{}/?status=NOK&{}'.format(
            Transaction.objects.order_by('id').last().token,
            urlencode({'error': 'پرداخت توسط کاربر لغو شد'})
        ))


@tag('backend')
class DepositBackendTest(DepositTest, TestCase):
    pass


@tag('ui')
@override_settings(**settings.TEST_SETTINGS)
class DepositSeleniumTest(DepositTest, SeleniumTestCase):

    def navigate_to_deposit_page(self):
        account_drop_down = self.client.web_driver.find_element_by_id('account')
        account_drop_down.click()
        charge_link = self.client.web_driver.find_element_by_link_text('شارژ حساب')
        link_path = charge_link.get_attribute('pathname')
        charge_link.click()
        return link_path

    def confirm_payment(self):
        self.selenium_client.web_driver.find_element_by_id('confirm').click()
        return SeleniumResponse(self.selenium_client.web_driver)

    def reject_payment(self):
        self.selenium_client.web_driver.find_element_by_id('reject').click()
        return SeleniumResponse(self.selenium_client.web_driver)

    def setUp(self):
        self.client = self.selenium_client
        super().setUp()


class TestWithdrawal(SetupUserAndAccountMixin):
    def test_withdrawal_request(self):
        # request withdrawal
        self.client.force_login(self.user)
        post_url = self.navigate_to_withdrawal_page()
        amount = self.prior_balance // 2
        response = self.client.post(post_url, data={'amount': amount}, follow=True)
        self.assertTrue('درخواست شما ثبت شد.' in response.content.decode('utf8'))
        transaction = Transaction.objects.last()
        self.client.logout()

        # approve withdrawal
        self.client.force_login(self.staff_user)
        post_url, response = self.navigate_to_withdrawal_approval_page()
        self.assertTrue(transaction.from_user.username in response.content.decode('utf8'))
        self.assertTrue(str(transaction.amount) in response.content.decode('utf8'))
        response = self.client.post(post_url, data={'verified': '1'}, follow=True)
        self.assertFalse(str(transaction.amount) in response.content.decode('utf8'))
        transaction.refresh_from_db()
        self.assertTrue(transaction.verified)
        self.assertEqual(Transaction.get_balance_from_user(self.user), self.prior_balance - amount)

    def navigate_to_withdrawal_approval_page(self):
        response = self.client.get('/accounts/withdrawal_approval/')
        self.assertEqual(response.status_code, 200)
        return '/accounts/transactions/{}/update/'.format(Transaction.objects.last().id), response

    def navigate_to_withdrawal_page(self):
        response = self.client.get('/accounts/withdrawals/')
        self.assertEqual(response.status_code, 200)
        return '/accounts/withdrawals/'

    def test_high_amount_validation(self):
        self.client.force_login(self.user)
        post_url = self.navigate_to_withdrawal_page()
        amount = self.prior_balance + 1
        response = self.client.post(post_url, data={'amount': amount}, follow=True)
        self.assertTrue('بیش از' in response.content.decode('utf8'))


@tag('backend')
class BackendWithdrawalTestCase(TestWithdrawal, TestCase):

    def test_transactions(self):
        response = self.client.get('/accounts/withdrawals/')
        self.assertNotEqual(response.status_code, 200)
        self.client.force_login(self.user)
        response = self.client.get('/accounts/withdrawals/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/accounts/withdrawal_approval/')
        self.assertNotEqual(response.status_code, 200)
        self.client.logout()
        self.client.force_login(self.staff_user)
        response = self.client.get('/accounts/withdrawal_approval/')
        self.assertEqual(response.status_code, 200)

    pass


@tag('ui')
@override_settings(**settings.TEST_SETTINGS)
class SeleniumWithdrawalTestCase(TestWithdrawal, SeleniumTestCase):

    def setUp(self):
        super().setUp()
        self.client = self.selenium_client

    def navigate_to_withdrawal_page(self):
        account_drop_down = self.client.web_driver.find_element_by_id('account')
        account_drop_down.click()
        charge_link = self.client.web_driver.find_element_by_link_text('برداشت از حساب')
        link_path = charge_link.get_attribute('pathname')
        charge_link.click()
        return link_path

    def navigate_to_withdrawal_approval_page(self):
        account_drop_down = self.client.web_driver.find_element_by_id('account')
        account_drop_down.click()
        charge_link = self.client.web_driver.find_element_by_link_text('تایید برداشت‌ها')
        link_path = charge_link.get_attribute('pathname')
        charge_link.click()
        return link_path, SeleniumResponse(self.client.web_driver)
