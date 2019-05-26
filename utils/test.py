import random
from copy import copy
from django.test import TestCase
from selenium.webdriver import Firefox

class SeleniumResponse(object):
    def __init__(self, web_driver):
        self.status_code = 404 if '404' in web_driver.page_source else 200
        self.content = web_driver.page_source
        self.web_driver = web_driver

class SeleniumDjangoTestClient(object):

    def __init__(self, web_driver=Firefox(), live_server_url=None):
        self.web_driver = web_driver
        self.live_server_url = live_server_url

    def get_absolute_url(self, path):
        return self.live_server_url + path

    def get(self, path):
        self.web_driver.get(path)
        return SeleniumResponse(self.web_driver)


    def post(self, path, data: dict = None):
        self.web_driver.get(path)
        last_element = None
        for name, value in data.items():
            element = self.web_driver.find_element_by_name(name)
            element.send_keys(value)
            last_element = element
        last_element.submit()

    def delete(self, path):
        self.get(path)
        return SeleniumResponse(self.web_driver)


class KakhneshinCRUDTestCase(TestCase):

    read_url = None
    list_url = None
    create_url = None
    delete_url = None
    update_url = None
    model = None
    model_test_data = ()
    visible_fields = ()

    def populate_with_test_data(self):
        result = []
        for model_test_data in self.model_test_data:
            instance = self.model(**model_test_data)
            instance.save()
            result.append(instance)
        return result

    def assert_object_in_response(self, obj, response):
        self.assert_object_page_ok_response(response)
        for visible_field in self.visible_fields:
            self.assertIn(
                str(getattr(obj, visible_field)), response.content.decode('utf8'),
                '{} read page does not contain visible field {}'.format(
                    self.model.name,
                    visible_field
                )
            )

    def assert_object_page_ok_response(self, response):
        self.assertEqual(
            response.status_code,
            200, '{} object page returned non OK status code.'.format(self.model.name)
        )

    def test_read(self):

        if self.read_url is None:
            return

        objs = self.populate_with_test_data()

        for obj in objs:
            response = self.client.get(self.read_url.format(obj.id))
            self.assert_object_in_response(obj, response)

    def test_list(self):

        if self.list_url is None:
            return

        objs = self.populate_with_test_data()

        response = self.client.get(self.list_url)

        for obj in objs:
            self.assert_object_in_response(obj, response)

    def test_create(self):
        for test_data in self.model_test_data:
            self.client.post(path=self.create_url, data=test_data)
            created_object = self.model.objects.order_by('id').last()
            self.assert_object_attributes(created_object, test_data)

    def assert_object_attributes(self, created_object, test_data):
        for field_name, value in test_data.items():
            self.assertEqual(getattr(created_object, field_name), value)

    def test_update(self):

        if self.update_url is None:
            return

        objs = self.populate_with_test_data()

        shuffled_test_data = copy(self.model_test_data)
        random.shuffle(shuffled_test_data)

        for obj_place, obj in enumerate(objs):
            response = self.client.post(
                path=self.update_url.format(obj.id),
                data=shuffled_test_data[obj_place],
                follow=True
            )
            self.assert_object_page_ok_response(response)
            obj.refresh_from_db()
            self.assert_object_attributes(obj, shuffled_test_data[obj_place])

    def test_delete(self):
        objs = self.populate_with_test_data()
        object_to_delete = random.choice(objs)
        self.client.get(path=self.delete_url.format(object_to_delete.id))
        self.assertTrue(self.model.objects.filter(id=object_to_delete.id).exists())
        self.client.post(path=self.delete_url.format(object_to_delete.id))
        self.assertFalse(self.model.objects.filter(id=object_to_delete.id).exists())
