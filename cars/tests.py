from django.test import TestCase
from rest_framework.reverse import reverse


class CarViewTests(TestCase):
    def test_create_success(self):
        resp = self.client.post(reverse('car-list'), {'make_name': 'fiat', 'model_name': 'brava'})
        self.assertEqual(resp.status_code, 201)

    def test_create_invalid_params(self):
        resp = self.client.post(reverse('car-list'), {'wrong': 'foo', 'data': 'bar'})
        self.assertEqual(resp.status_code, 400)

        want = {'make_name': ['This field is required.'], 'model_name': ['This field is required.']}
        self.assertEqual(resp.json(), want)
