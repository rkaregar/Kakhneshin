from django.test import LiveServerTestCase
from habitats.models import Habitat
from selenium import webdriver

# Create your tests here.
from utils.test import KakhneshinCRUDTestCase, SeleniumDjangoTestClient


class HabitatsBackendTest(KakhneshinCRUDTestCase):
    read_url = '/habitats'
    list_url = '/habitats'
    create_url = '/habitats/create'
    update_url = '/habitats/update'
    delete_url = '/habitats/delete'

    model = Habitat
    model_test_data = [
        {
            'name': 'اقامتگاه اول',
            'address': 'اول آنجایی که می‌دانی',
            'town': 'تهران',
            'cost': 100000,
        }
    ]
    visible_fields = ('name', 'address', 'town', 'cost')


class HabitatSeleniumTest(LiveServerTestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        driver_options = webdriver.ChromeOptions()
        driver_options.add_argument('--headless')
        driver_options.add_argument('--no-sandbox')
        driver_options.add_argument('--disable-dev-shm-usage')
        self.client = SeleniumDjangoTestClient(web_driver=webdriver.Chrome(chrome_options=driver_options),
                                               live_server_url=self.live_server_url)
