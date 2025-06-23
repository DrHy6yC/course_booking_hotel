from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.repositories.mappers.base import DataMapper
from src.schemas.booking import Booking
from src.schemas.facility import Facility, RoomFacility
from src.schemas.hotel import Hotel
from src.schemas.room import Room, RoomWithRels
from src.schemas.user import User


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Room


class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomWithRels


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesORM
    schema = RoomFacility


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facility
