from napalm import get_network_driver
import json
from netmiko import Netmiko


#WE HAVE SPECIFY SOFTWARE BELOW
driver = get_network_driver('ios')

#ENABLE PASSWORD
enable_pass = {'secret': 'cisco'}

#IP, LOGIN, PASSWORD, ENABLE PASS
IP = '10.101.1.2'
ios = driver(IP, 'admin', 'admin', optional_args=enable_pass)

#OPEN CONNECTION
ios.open()

#YOUR CODE
output = ios.get_interfaces()
#dump = json.dumps(output, indent = 4)       #INDENT - NICE FORMAT

interfaces = []

for key, value in output.items():
    interfaces.extend([key])

###### DELETING ALL VLAN INTERFACE IF EXIST IN OUR LIST (NOT DEVICE!!!)####################
for x in interfaces:
    if 'Vlan1' in interfaces:
      interfaces.pop(-1)

#CLOSING CONNECTION
ios.close()

######################CONNECT TO DEVICE################################
connection = Netmiko(host='10.101.1.2', port='22', username='admin', password='admin', device_type='cisco_ios')

#######################BACKUP CREATION###############################
backup = connection.send_command('show running-config')
backup = backup[100:]           #DEPENDS ON DEVICE OUTPUT

with open('backup.txt', 'w') as f:
    f.write(backup)                     #IT APPEARS WHEN THE WHOLE SCRIP EXECUTE

######################VLAN CHECK################################
output = connection.send_command('show vlan brief')
if not '10' in output:
    output = connection.send_command('conf t')
    output = connection.send_command('vlan 10')
    output = connection.send_command('exit')
elif not '20' in output:
    output = connection.send_command('conf t')
    output = connection.send_command('vlan 20')
    output = connection.send_command('exit')
elif not '30' in output:
    output = connection.send_command('conf t')
    output = connection.send_command('vlan 30')
    output = connection.send_command('exit')

port_status = {'interface': {'TIME': "STATUS"}}
#####################INTERFACE CECK#############################
for interface in interfaces:
    status = connection.send_command(f'show interface {interface}')
    output = connection.send_command(f'show running-config | s interface {interface}')
    print(interface)
    port_status.update({interface: {}})

    #####INTERFACE STATUS UP/DOWN#################################
    if 'is up' in status:
        print('Currently port is UP!')                    ####
        port_status[interface]['BEFORE'] = 'UP'
    else:
        print('Currently port is DOWN!')
        port_status[interface]['BEFORE'] = 'DOWN'

    ##########NAC CHECK###########################################
    if 'authentication open' in status:
        nac_status = 1                              #1 - NAC DISABLED
    else:
        nac_status = 2

    ##########VLAN CHECK AND ADDING PROPER CONFIGURATION##########
    if 'switchport access vlan 10' in output:
        print("Interface is in vlan 10, adding not exist commands...")
        commands = ['conf t', f' default interface {interface}', f'interface {interface}', 'description OFFICE', 'switchport mode access', 'switchport access vlan 10', 'exit']
        connection.send_config_set(commands)

    elif 'switchport access vlan 20' in output:
        print("Interface is in vlan 20, adding not exist commands...")
        commands = ['conf t', f' default interface {interface}', f'interface {interface}', 'description INDUSTIRAL 20', 'switchport mode access', 'switchport access vlan 20', 'exit']
        connection.send_config_set(commands)

    elif 'switchport access vlan 30' in output:
        print("Interface is in vlan 30, adding not exist commands...")
        commands = ['conf t', f' default interface {interface}', f'interface {interface}', 'description R&D', 'switchport mode access', 'switchport access vlan 30', 'exit']
        connection.send_config_set(commands)

    else:
        print("PORT IS IN DEFAULT VLAN!")
        print("Description set to 'BLACKHOLE'")
        commands = ['conf t', f'interface {interface}', 'description BLACKHOLE', 'exit']
        connection.send_config_set(commands)

    ##############NAC CONFIGURATION#######################
    if nac_status == 1:
        print(f"Auth open was previously set on this port, I am sending 'auth open' to {interface}")
        commands = ['conf t', f'interface {interface}', 'no auth open', 'exit']
        connection.send_config_set(commands)
    elif nac_status == 2:
        print(f"Auth open wasn't previously set on this port.")

    ###############CHECKING STATUS AND AUTH AFTER UPDATE#############################
    output = connection.send_command(f'show running-config | s interface {interface}')
    if 'is up' in status:
        print('Currently port is UP!')
        port_status[interface]['AFTER'] = "UP"
    else:
        print('Currently port is DOWN!')
        port_status[interface]['AFTER'] = "DOWN"

    print(30 * '#')


dump = json.dumps(port_status, indent = 4)       #INDENT - NICE FORMAT
print(dump)


########CLOSING SECOND SSH CONNECTION############
connection.disconnect()

print(30 * '#')
print(f'Switch {IP} successfully configured!')