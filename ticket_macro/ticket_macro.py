from SRT import *
from korail2 import *

from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


KST = timezone(timedelta(hours=9))


class Platform(Enum):
    SR = 0
    KORAIL = 1


# class Preference(Enum):
#     ANY = 0
#     AISLE = 1
#     WINDOW = 2


def get_date() -> str:
    return datetime.now(KST).strftime('%Y%m%d')


def get_time() -> str:
    return datetime.now(KST).strftime('%H%M00')


@dataclass
class Reservation:
    dep: str
    arr: str
    date: str | None = get_date()
    time: str | None = get_time()
    time_limit: str | None = None


@dataclass
class SRReservation(Reservation):
    passengers: list[Passenger] | None = None
    reserve_option: SeatType = SeatType.GENERAL_FIRST
    window: bool | None = None

    def __repr__(self) -> str:
        return f'[SR] {self.__dict__}'


@dataclass
class KorailReservation(Reservation):
    train_type: TrainType = TrainType.ALL
    passengers: list[Passenger] = None
    reserve_option: ReserveOption = None

    def __repr__(self) -> str:
        return f'[KORAIL] {self.__dict__}'


class TrainMacro():
    def __init__(self, reservation: Reservation, username: str | None = None, password: str | None = None, login: bool = False) -> None:
        self.reservation = reservation
        self.username = username
        self.password = password

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
                trains = self.api.search_train_allday(
                    dep=self.reservation.dep,
                    arr=self.reservation.arr,
                    date=self.reservation.date,
                    time=self.reservation.time,
                    train_type=self.reservation.train_type,
                    passengers=self.reservation.passengers,
                    include_no_seats=(not available_only)
                )

                if self.reservation.time == None:
                    self.reservation.time = '000000'

                if self.reservation.time_limit == None:
                    return trains
                else:
                    return [train for train in trains if int(self.reservation.time) <= int(train.dep_time) <= int(self.reservation.time_limit)]

        return []


if __name__ == '__main__':
    print('This is a temporary test.')
    ktx = KorailReservation('서울', '부산', '20230802', '000000', '053000', train_type=TrainType.KTX)
    srt = SRReservation('수서', '부산')

    print(ktx)
    print(srt)

    ktx_macro = TrainMacro(ktx)
    srt_macro = TrainMacro(srt)

    print()
    print(ktx_macro.search())
    print()
    print(srt_macro.search())