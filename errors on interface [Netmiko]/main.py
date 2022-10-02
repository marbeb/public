from netmiko import Netmiko
import re
import getpass

IP = input('Enter device address IP: ')
login = input('Enter login: ')
password = getpass.getpass('Enter password: ')

#########NETMIKO CONNECTION#######################
connection = Netmiko(host=IP, port='22', username=login, password=password, device_type='cisco_ios')

interfaces = connection.send_command('show running | i interface')
interfaces = interfaces.splitlines()

if 'interface Vlan1' in interfaces:
    interfaces.pop(-1)

##############ALL OUTPUT TO FILE################
file = open('script_log.txt', 'a')

for interface in interfaces:
    counters = connection.send_command(f'show {interface}')
    counters = counters.splitlines()
    last_cleaning = counters[12]
    counters = counters[21]
    file.write('###################### \n')
    print(interface)
    file.write(interface + '\n')
    print(last_cleaning)
    file.write(last_cleaning + '\n')
    print(counters)
    file.write(counters + '\n')
    intf = interface[10:]

    counters = '   10 input errors, 10 CRC, 0 frame, 0 overrun, 0 ignored'
    #################################
    input_errors = re.search("[^1-9][0] input", counters)
    crc_errors = re.search("[^1-9][0] CRC", counters)
    ######################################

    if not input_errors and not crc_errors:
        print(f'There are INPUT AND CRC ERRORS on the {interface}, cleaning..')
        connection.send_command(f'clear counters {intf}', '\n')
        print('Counters successfully cleared!')
        file.write('Counters have been cleared.\n')
    elif not input_errors:
        print(f'  There ARE INPUT ERRORS on the {interface}, cleaning...')
        connection.send_command(f'clear counters {intf}', '\n')
        print('Counters successfully cleared!')
        file.write('Counters have been cleared.\n')
    elif not crc_errors:
        print(f'  There ARE CRC ERRORS on the {interface}, cleaning...',)
        connection.send_command(f'clear counters {intf}', '\n')
        print('Counters successfully cleared!')
        file.write('Counters have been cleared.\n')
    else:
        print(f"  There are NO ERRORS on {intf}")

    print(30*'#')




print(f'Closing file and SSH connection with {IP}')
file.close()
connection.disconnect()

