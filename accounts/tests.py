from accounts.models import Transaction
from django.contrib.auth.models import User
from django.test import TestCase, tag
from utils.test import create_user


class DepositTest:

    def setUp(self):
        super().setUp()
        self.user = create_user()
        self.prior_balance = 12143
        Transaction.objects.create(to_user=self.user, amount=self.prior_balance, verified=True)

    def test_deposit(self):
        response = self.client.get('/accounts/deposit/')
        self.assertEqual(response.status_code, 200)
        amount = 1452
        response = self.client.post('/accounts/deposit/', data={'amount': amount}, follow=True)
        self.assertTrue('شارژ حساب با موفقیت انجام شد.' in response.body.decode('utf8'))
        self.assertTrue(str(amount + self.prior_balance) in response.body.decode('utf8'))



@tag('backend')
class DepositBackendTest(DepositTest, TestCase):
    pass