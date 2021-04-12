import ipaddress
import sys

pyVersion = int(sys.version[0])

if int(pyVersion) < 3:
    input_from_keyboard = raw_input
else:
    input_from_keyboard = input


# user defined function:
# name: ip_input_format(string_tag)
# input: string_tag: string_tag for ip address input
# function: returns Host IP address after checking the correct format
def ip_input_format(string_tag):
    while (True):
        ip_address = input_from_keyboard(string_tag)
        if (ip_address.upper() == 'Q'):
            exit(-1)
        if pyVersion < 3:                               # requires to decode the key_board input for ip
            ip_address = ip_address.decode('utf-8')     # applicable to "ipaddress" library for Python 2.x.x
        try:
            ipaddress.ip_address(ip_address)
            # socket.inet_aton(ip_address)
            # printl(ip_address)
            break
        except Exception as e:
            print(str(e))
            print("{}: Invalid IP Input. ---Try Again---'".format(ip_address))
            #exit(-1)
    return ip_address

def generate_net_id_from_loopback0(Loopback):
    ip_octates = Loopback.split('.')
    loopback_len = len(ip_octates)

    sys_id_1 = ''
    if (loopback_len == 4):
        for oc in ip_octates:
            if len(oc) == 1:
                sys_id_1 = sys_id_1 + '00' + oc
            elif len(oc) == 2:
                sys_id_1 = sys_id_1 + '0' + oc
            else:
                sys_id_1 = sys_id_1 + oc

    len_toc = len(sys_id_1)
    # print(len_toc)
    len_ned_oc = int(len_toc / 4)
    SYSTEM_ID = ''
    for i in range(len_toc):
        SYSTEM_ID = SYSTEM_ID + sys_id_1[i]
        if (i == 3 or i == 7):
            SYSTEM_ID = SYSTEM_ID + '.'


    return SYSTEM_ID

'''Example of standalone use of this file====
--------------------------------------------------
while(True):
    Loopback = ip_input_format('Enter Loopback 0 IP Address (enter q/Q to exit): ')


    print(generate_net_id_from_loopback0(Loopback))
'''