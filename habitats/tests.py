from django.test import TestCase
from .models import *


class RoomOutOfServiceTest(TestCase):
    def setUp(self):
        habitat = Habitat.objects.create(name='test habitat')
        self.room = RoomType.objects.create(habitat=habitat, type_name='test room', capacity_in_person=4,
                                            number_of_rooms_of_this_kind=4)

    def test_out_of_service_without_any_constraint(self):
        self.assertTrue(self.room.is_limitation_valid('2019-10-10', '2019-10-15', 2))

    def test_room_is_limitation_valid_after_adding_out_of_service(self):
        RoomOutOfService.objects.create(room=self.room, inclusive_since='2019-10-10', exclusive_until='2019-10-15',
                                        number_of_affected_rooms=2)
        self.assertTrue(self.room.is_limitation_valid('2019-10-05', '2019-10-25', 2))

    def test_out_of_service_more_than_number_of_rooms(self):
        with self.assertRaises(ValidationError):
            RoomOutOfService.objects.create(room=self.room, inclusive_since='2019-10-10', exclusive_until='2019-10-15',
                                            number_of_affected_rooms=5)

    def test_room_out_of_service_exclude_until(self):
        RoomOutOfService.objects.create(room=self.room, inclusive_since='2019-10-10', exclusive_until='2019-10-15',
                                        number_of_affected_rooms=3)
        self.assertTrue(self.room.is_limitation_valid('2019-10-15', '2019-10-20', 3))

    def test_out_of_service_include_since(self):
        RoomOutOfService.objects.create(room=self.room, inclusive_since='2019-10-10', exclusive_until='2019-10-15',
                                        number_of_affected_rooms=3)
        with self.assertRaises(ValidationError):
            RoomOutOfService.objects.create(room=self.room, inclusive_since='2019-10-14', exclusive_until='2019-10-20',
                                            number_of_affected_rooms=3)

    def test_prevent_adding_out_of_service_include_since_reservation(self):
        Reservation.objects.create(from_date='2019-10-10', to_date='2019-10-15', is_active=True, room=self.room)
        Reservation.objects.create(from_date='2019-10-10', to_date='2019-10-15', is_active=True, room=self.room)

        with self.assertRaises(ValidationError):
            RoomOutOfService.objects.create(room=self.room, inclusive_since='2019-10-05', exclusive_until='2019-10-11',
                                            number_of_affected_rooms=3)

    def test_add_out_of_service_exclude_until_reservation(self):
        Reservation.objects.create(from_date='2019-10-10', to_date='2019-10-15', is_active=True, room=self.room)
        Reservation.objects.create(from_date='2019-10-10', to_date='2019-10-15', is_active=True, room=self.room)

        self.assertTrue(self.room.is_limitation_valid('2019-10-15', '2019-10-20', 3))

    def test_add_out_of_service_ignore_inactive_reservations(self):
        Reservation.objects.create(from_date='2019-10-10', to_date='2019-10-15', is_active=True, room=self.room)
        Reservation.objects.create(from_date='2019-10-10', to_date='2019-10-15', is_active=True, room=self.room)
        Reservation.objects.create(from_date='2019-10-10', to_date='2019-10-15', is_active=False, room=self.room)
        Reservation.objects.create(from_date='2019-10-10', to_date='2019-10-15', is_active=False, room=self.room)

        self.assertTrue(self.room.is_limitation_valid('2019-10-10', '2019-10-20', 2))

    def test_add_out_of_service_with_previous_limitations_and_reservations(self):
        Reservation.objects.create(from_date='2019-10-05', to_date='2019-10-10', is_active=True, room=self.room)
        Reservation.objects.create(from_date='2019-10-10', to_date='2019-10-15', is_active=True, room=self.room)
        Reservation.objects.create(from_date='2019-10-10', to_date='2019-10-15', is_active=True, room=self.room)
        Reservation.objects.create(from_date='2019-10-15', to_date='2019-10-20', is_active=True, room=self.room)

        RoomOutOfService.objects.create(room=self.room, inclusive_since='2019-10-05', exclusive_until='2019-10-10',
                                        number_of_affected_rooms=1)
        RoomOutOfService.objects.create(room=self.room, inclusive_since='2019-10-15', exclusive_until='2019-10-20',
                                        number_of_affected_rooms=1)
        RoomOutOfService.objects.create(room=self.room, inclusive_since='2019-10-05', exclusive_until='2019-10-20',
                                        number_of_affected_rooms=1)

        self.assertTrue(self.room.is_limitation_valid('2019-10-05', '2019-10-20', 1))
