from SRT import *
from korail2 import *

from enum import Enum
from datetime import date
from dataclasses import dataclass


class Platform(Enum):
    SR = 0
    KORAIL = 1


class Preference(Enum):
    ANY = 0
    AISLE = 1
    WINDOW = 2


@dataclass
class Reservation:
    dep: str = None
    arr: str = None
    date: str = date.today().strftime('%Y%m%d')
    time: str = '000000'
    time_limit: str = None


@dataclass
class SRReservation(Reservation):
    passengers: list[Passenger] = None
    reserve_option: SeatType = None
    preference: str = None


@dataclass
class KorailReservation(Reservation):
    train_type: TrainType = TrainType.ALL
    passengers: list[Passenger] = None
    reserve_option: ReserveOption = None


print(Reservation.date)