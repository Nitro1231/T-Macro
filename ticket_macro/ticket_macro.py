from SRT import *


class TicketMacro:
    def __init__(self, login: dict, notification: dict, reservations: list[dict]) -> None:
        self.sr = None
        self.korail = None

        if 'sr' in login:
            self.sr = SRT(login['sr']['username'], login['sr']['password'], False)
        if 'korail' in login:
            self.korail = Korail(login['korail']['username'], login['korail']['password'], False)
        
        self.notification = list()
        



