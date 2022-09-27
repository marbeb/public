#PROGRAM KTÓRY: PYTA ILE URZADZEN - TE IP WPISUJESZ
#NASTĘPNIE DO KAŻDEGO Z TEGO IP WRZUCA KOMENDY JAKIE ZNAJDUJĄ SIE W COMMANDS.txt
#COMMANDS.TXT - KAZDA KOMENDA W OSOBNEJ LINIJCE

import time
import paramiko

lista_ip = []

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


amount = input("Ile sprzętów?")
amount = int(amount)

for x in range(amount):
    ip = input('Podaj IP:')
    lista_ip.extend([ip])

print(lista_ip)

with open('commands.txt') as f:
    commands = f.read().splitlines()

for host in lista_ip:
    ssh_client.connect(hostname=host, port='22', username='admin', password='admin', look_for_keys=False, allow_agent=False)
    shell = ssh_client.invoke_shell()

    for command in commands:
        shell.send(f'{command}' + '\n')
        time.sleep(1)

    output = shell.recv(1000000)
    output = output.decode()
    print(output)


ssh_client.close()