import os.path
import networking.nettools as nt

CFG_PATH = os.path.join(os.path.expanduser("~"), ".config", "net-scanner.conf")


def create_cfg():
    print("Config file not detected")
    print("Generating new one...")
    sender_mail = input("Enter mail used by script: ")
    password_mail = input("Enter mail password: ")
    receiver_mail = input("Enter receiver mail: ")
    print("=== SCANNED INTERFACE ===")

    i = 1
    interfaces = nt.get_interfaces()
    for interface in interfaces:
        print("{}. {}".format(i, interface))
        i += 1

    index_number = int(input("Choose interface (number): "))

    chosen_interface = interfaces[index_number - 1]

    with open(CFG_PATH, newline='', mode='w') as file:
        file.write(sender_mail + '\n')
        file.write(password_mail + '\n')
        file.write(receiver_mail + '\n')
        file.write(chosen_interface["name"] + '\n')
        file.write(chosen_interface["address"] + '\n')
        file.write(chosen_interface["mask"] + '\n')


def load_config():

    if not os.path.exists(CFG_PATH):
        create_cfg()

    sender_mail = password_mail = receiver_mail = None
    interface = {}

    with open(CFG_PATH, newline='', mode='r') as file:
        sender_mail = file.readline().rstrip()
        password_mail = file.readline().rstrip()
        receiver_mail = file.readline().rstrip()
        interface["name"] = file.readline().rstrip()
        interface["address"] = file.readline().rstrip()
        interface["mask"] = file.readline().rstrip()

    return [sender_mail, password_mail, receiver_mail, interface]
