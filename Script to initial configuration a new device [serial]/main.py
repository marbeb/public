import serial
import time

##############################################
hostname = input('Enter hostname: ')
login = input('Enter local user login: ')
password = input('Enter local user password: ')
vlan_mgmt = input("Enter MGMT vlan ID: ")
IP = input("Enter mgmt IP address: ")
uplink = input("Enter uplink interface: ")
com = input('Enter port com number: ')
###############################################

def open_console(port=f'com{5}', boudrate = 9600):
    console = serial.Serial(port='com5', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=8)
    if console.isOpen():
        print('Connected to device via console.')
        return console
    else:
        print("Can't connect to this device using console cable, check com port!")
        return False

def run_command(console, cmd='\n', sleep=2):
    print('Sending command: ' + cmd)
    console.write(cmd.encode() + b'\n')
    time.sleep(sleep)

def read_from_console(console):
    bytes_to_be_read = console.inWaiting()
    if bytes_to_be_read:
        output = console.read(bytes_to_be_read)
        return output.decode()
    else:
        return False

def inital_configuration_dialog(console):
	run_command(console, '\n')
	prompt = read_from_console(console)
	if 'Would you like to enter the initial configuration dialog?' in prompt:
		run_command(console, 'no', 20)
		run_command(console, '\n')
		return True
	else:
		return False

##############################################################################################

console = open_console()
inital_configuration_dialog(console)

comm = ['enable', 'conf t', f'username {login} privilege 15 secret {password}',f'hostname {hostname}', f'vlan {vlan_mgmt}', 'name Infra', 'exit', f'interface vlan {vlan_mgmt}', f'ip address {IP} 255.255.255.0', 'no shut', f'exit', f'interface {uplink}', 'switch port mode trunk', 'exit']

for line in comm:
    run_command(console, line)

with open('config.txt') as f:
	commands = f.readlines()
	####COMMANDS IS A LIST WITH COMMANDS NOW
	for cmd in commands:
		run_command(console, cmd)

#URGENT! CLOSING SERIAL CONNECTION! TYPE END, EXIT IN TXT!

print(f'IP ADDRESS: {IP}, SSH V2 ENABLED!')
print('DEVICE CONFIGURED SUCCESSFULLY!')
time.sleep(5)