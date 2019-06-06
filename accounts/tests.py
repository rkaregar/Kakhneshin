from accounts.models import Transaction
from django.contrib.auth.models import User
from django.test import TestCase, tag, LiveServerTestCase
from utils.test import create_user, SeleniumTestCase


class DepositTest:

    def setUp(self):
        super().setUp()
        self.user = create_user()
        self.client.login(username='test', password='test')
        self.prior_balance = 12143
        Transaction.objects.create(to_user=self.user, amount=self.prior_balance, verified=True)

    def test_deposit(self):
        post_url = self.navigate_to_deposit_page()
        amount = 1452
        response = self.client.post(post_url, data={'amount': amount}, follow=True)
        self.assertTrue('شارژ حساب با موفقیت انجام شد.' in response.content.decode('utf8'))
        self.assertTrue(str(amount + self.prior_balance) in response.content.decode('utf8'))

    def navigate_to_deposit_page(self):
        response = self.client.get('/accounts/deposit/')
        self.assertEqual(response.status_code, 200)
        return '/accounts/deposit/'


@tag('backend')
class DepositBackendTest(DepositTest, TestCase):
    pass

@tag('ui')
class DepositSeleniumTest(DepositTest, SeleniumTestCase):

    def navigate_to_deposit_page(self):
        account_drop_down = self.client.web_driver.find_element_by_id('account')
        account_drop_down.click()
        charge_link = self.client.web_driver.find_element_by_link_text('شارژ حساب')
        link_path = charge_link.get_attribute('pathname')
        charge_link.click()
        return link_path

    def setUp(self):
        self.client = self.selenium_client
        super().setUp()
