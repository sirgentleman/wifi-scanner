import nettoolbox as ntb
from networking.network_state import NetworkState
from mail.mail_service import MailService
from config import *


def main():

    sender_mail, password_mail, receiver_mail, interface = load_config()

    service = MailService(sender_mail, password_mail, receiver_mail)

    state = NetworkState(interface)
    state.load_map()

    state.scan()
    state.save_map()
    service.send_curr_state(state.curr_connected)


if __name__ == "__main__":
    main()
