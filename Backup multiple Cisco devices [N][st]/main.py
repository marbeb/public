from netmiko import ConnectHandler
from datetime import datetime

now = datetime.now()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute

with open('devices_to_backup.txt') as f:
    devices = f.read().splitlines()

for IP in devices:
    cisco_device = {
            'device_type': 'cisco_ios',
            'host': IP,
            'username': 'admin',
            'password': 'admin',
            'port': 22,
            'secret': 'cisco',
            'verbose': True
            }

    connection = ConnectHandler(**cisco_device)
    output = connection.send_command('show running-config')
    prompt = connection.find_prompt()
    hostname = prompt[:-1]

    file_name = f'{hostname}-{year}-{month}-{day}-{hour};{minute}.txt'
    output = output[61:]

    with open(file_name, 'w') as f:
        f.write(output)
        print(30 * '#')
        print(f'Backup of {hostname} completed!')
        print(30 * '#')

    print('Disconnecting...')
    connection.disconnect()
