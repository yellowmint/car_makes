from django.test import TestCase
from rest_framework.reverse import reverse

from cars.models import Car, Rate


class CarViewTests(TestCase):
    def test_create_success(self):
        resp = self.client.post(reverse('car-list'), {'make_name': 'fiat', 'model_name': 'brava'})
        self.assertEqual(resp.status_code, 201)

    def test_create_not_existing_car(self):
        resp = self.client.post(reverse('car-list'), {'make_name': 'fiat', 'model_name': 's60'})
        self.assertEqual(resp.status_code, 400)

        want = {'non_field_errors': ['given make and model not exist in reality and cannot be saved']}
        self.assertEqual(resp.json(), want)

    def test_create_invalid_params(self):
        resp = self.client.post(reverse('car-list'), {'wrong-key': 'foo', 'model_name': 'a' * 251})
        self.assertEqual(resp.status_code, 400)

        want = {
            'make_name': ['This field is required.'],
            'model_name': ['Ensure this field has no more than 250 characters.']
        }
        self.assertEqual(resp.json(), want)

    def test_list_empty(self):
        resp = self.client.get(reverse('car-list'))
        self.assertEqual(resp.json(), [])

    def test_list_filled(self):
        fiat = Car.objects.create(make_name='fiat', model_name='brava')
        opel = Car.objects.create(make_name='opel', model_name='ampera')
        Rate.objects.create(car=opel, value=4)
        Rate.objects.create(car=opel, value=5)

        resp = self.client.get(reverse('car-list'))
        want = [
            {'id': opel.id, 'make_name': 'opel', 'model_name': 'ampera', 'average_rate': 4.5, 'rates_count': 2},
            {'id': fiat.id, 'make_name': 'fiat', 'model_name': 'brava', 'average_rate': None, 'rates_count': 0}
        ]
        self.assertEqual(resp.json(), want)


class PopularViewTests(TestCase):
    def test_list_empty(self):
        resp = self.client.get(reverse('popular-list'))
        self.assertEqual(resp.json(), [])

    def test_list_filled(self):
        fiat = Car.objects.create(make_name='fiat', model_name='brava')
        Rate.objects.create(car=fiat, value=3)

        opel = Car.objects.create(make_name='opel', model_name='ampera')
        Rate.objects.create(car=opel, value=3)
        Rate.objects.create(car=opel, value=4)
        Rate.objects.create(car=opel, value=4)

        volvo = Car.objects.create(make_name='volvo', model_name='v60')
        Rate.objects.create(car=volvo, value=4)
        Rate.objects.create(car=volvo, value=5)

        Car.objects.create(make_name='audi', model_name='a4')

        resp = self.client.get(reverse('popular-list'))
        want = [
            {'id': opel.id, 'make_name': 'opel', 'model_name': 'ampera', 'average_rate': 3.67, 'rates_count': 3},
            {'id': volvo.id, 'make_name': 'volvo', 'model_name': 'v60', 'average_rate': 4.5, 'rates_count': 2},
            {'id': fiat.id, 'make_name': 'fiat', 'model_name': 'brava', 'average_rate': 3.0, 'rates_count': 1},
        ]
        self.assertEqual(resp.json(), want)


class RateViewTests(TestCase):
    def setUp(self):
        self.car = Car.objects.create(make_name='fiat', model_name='brava')

    def test_create_success(self):
        resp = self.client.post(reverse('rate-list'), {'car': self.car.id, 'value': 3})
        self.assertEqual(resp.status_code, 201)

    def test_create_invalid_car_id(self):
        resp = self.client.post(reverse('rate-list'), {'car': -1, 'value': 3})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'car': ['Invalid pk "-1" - object does not exist.']})

    def test_create_min_value(self):
        resp = self.client.post(reverse('rate-list'), {'car': self.car.id, 'value': 0})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'value': ['Ensure this value is greater than or equal to 1.']})

    def test_create_max_value(self):
        resp = self.client.post(reverse('rate-list'), {'car': self.car.id, 'value': 6})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'value': ['Ensure this value is less than or equal to 5.']})
