from django.test import LiveServerTestCase
from habitats.models import Habitat

# Create your tests here.
from utils.test import KakhneshinCRUDTestCase, SeleniumDjangoTestClient


class HabitatsBackendTest(KakhneshinCRUDTestCase):

    read_url = '/habitats'
    list_url = '/habitats'
    create_url = '/habitats/create'
    update_url = '/habitats/update'
    delete_url = '/habitats/delete'

    model = Habitat
    model_test_data = (
        {
            'name': 'اقامتگاه اول',
            'address': 'اول آنجایی که می‌دانی',
            'town': 'تهران',
            'cost': 100000,
        }
    )
    visible_fields = ('name',)


class HabitatSeleniumTest(LiveServerTestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.client = SeleniumDjangoTestClient(live_server_url=self.live_server_url)