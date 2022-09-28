from napalm import get_network_driver
from netmiko import Netmiko
import json

#WE HAVE SPECIFY SOFTWARE BELOW
driver = get_network_driver('ios')

#ENABLE PASSWORD
enable_pass = {'secret': 'cisco'}

#IP, LOGIN, PASSWORD, ENABLE PASS
ios = driver('10.101.1.2', 'admin', 'admin', optional_args=enable_pass)

#OPEN CONNECTION
ios.open()

#YOUR CODE
output = ios.get_interfaces_counters()

#########NETMIKO CONNECTION#######################
connection = Netmiko(host='10.101.1.2', port='22', username='admin', password='admin', device_type='cisco_ios')

####################COUNTERS#########################
for interface in output:
    if 'Vlan' in interface:
        break
    print('########', interface, '########')
    interface_counters = connection.send_command(f'show interface {interface}')
    interface_counters = interface_counters.splitlines()
    interface_counters = interface_counters[21]
    #interface_counters = '0 input errors, 11 CRC, 0 frame, 0 overrun, 0 ignored'
    print(interface_counters)

    ############LAST CLEAR COUNTER#################
    last_clear = connection.send_command(f'show interface {interface}')
    last_clear = last_clear.splitlines()
    last_clear = last_clear[12]
    print('  ', last_clear)

    if not '0 input errors' in interface_counters:
        print(f'     There are INPUT errors on the {interface}, cleaning..."')
        connection.send_command(f'clear counters interface {interface}')
    elif not '0 CRC' in interface_counters:
        print(f'     There are CRC errors on the {interface}, cleaning..."')
        connection.send_command(f'clear counters interface {interface}')
    else:
        print(f"     There are no errors on {interface}")

    ##############INTERFACE STATUS#################
    interface_status = connection.send_command(f'show interface {interface}')
    if 'is up' in interface_status:
        print(f'     Interface is up!')
    elif 'is down' in interface_status:
        print(f'     Interface is down!')


#CLOSING CONNECTION
ios.close()
connection.disconnect()