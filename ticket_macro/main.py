import tools
from ticket_macro import TicketMacro


OPTION = '../option.json'
EMAIL = '../email.json'


if __name__ == '__main__':
    option = tools.read_json(OPTION)
    email = tools.read_json(EMAIL)
    