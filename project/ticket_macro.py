from SRT import *
from korail2 import *

from enum import Enum
from dataclasses import dataclass


class Platform(Enum):
    SR = 0
    KORAIL = 1


# class Preference(Enum):
#     ANY = 0
#     AISLE = 1
#     WINDOW = 2


@dataclass
class Reservation:
    dep: str
    arr: str
    date: str | None = None
    time: str | None = None


@dataclass
class SRReservation(Reservation):
    time_limit: str | None = None
    passengers: list[Passenger] | None = None
    reserve_option: SeatType = SeatType.GENERAL_FIRST
    window: bool | None = None

    def __str__(self) -> str:
        return f'[SR] {self.__dict__}'


@dataclass
class KorailReservation(Reservation):
    train_type: TrainType = TrainType.ALL
    passengers: list[Passenger] = None
    reserve_option: ReserveOption = None

    def __str__(self) -> str:
        return f'[KORAIL] {self.__dict__}'


class TrainMacro():
    def __init__(self, username: str, password: str, reservation: Reservation, login: bool = False) -> None:
        self.username = username
        self.password = password
        self.reservation = reservation
        
        if type(reservation) == SRReservation:
            self.platform = Platform.SR
            self.api = SRT(username, password, login)
        elif type(reservation) == KorailReservation:
            self.platform = Platform.KORAIL
            self.api = Korail(username, password, login)
        else:
            raise ValueError


    def __str__(self) -> str:
        return str(self.reservation)


    def search(self, available_only: bool = True) -> list:
        match self.platform:
            case Platform.SR:
                return self.api.search_train(
                    dep=self.reservation.dep,
                    arr=self.reservation.arr,
                    time=self.reservation.time,
                    time_limit=self.reservation.time_limit,
                    available_only=available_only
                )
            case Platform.KORAIL:
                return self.api.search_train(
                    dep=self.reservation.dep,
                    arr=self.reservation.arr,
                    date=self.reservation.date,
                    time=self.reservation.time,
                    train_type=self.reservation.train_type,
                    passengers=self.reservation.passengers,
                    include_no_seats=(not available_only)
                )
        raise ValueError


ktx = KorailReservation('서울', '부산', train_type=TrainType.KTX)
srt = SRReservation('수서', '부산')

ktx_macro = TrainMacro(None, None, ktx)
srt_macro = TrainMacro(None, None, srt)

print(ktx_macro.search())
print()
print(srt_macro.search())