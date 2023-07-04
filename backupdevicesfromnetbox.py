#########################################
#            BACKUP SCRIPT              #
#  CISCO ARUBA DELL HP FORTINET JUNOS   #
#           by marcin.bebenek           #
#########################################
import pynetbox
from netmiko import ConnectHandler
from paramiko.ssh_exception import AuthenticationException
from netmiko import NetmikoTimeoutException
from netmiko import NetmikoAuthenticationException
from datetime import datetime
import time
import smtplib, ssl
from email.message import EmailMessage


device_with_tag = []         #Lista sprzętu z tagiem 'backup' jaka skrypt pobrał z netboxa
devices_to_backup = {}       #Dictionary na podstawie devices_to_backup z odpowiednio: hostname: IP
success = []
fail = []
amountf = []
file_notexist = []
file_exist = []

now = datetime.now()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute

### Ladne wyswietlanie czasu
if minute < 10:
    minute = f'0{minute}'
    
if hour < 10:
    hour = f'0{hour}'
    
if month < 10:
    month = f'0{month}'

if day < 10:
    day = f'0{day}'
    
def powiadomienie(body, email_receiver):
    ############################################################
    subject = f'NETWORK - BACKUP STATUS DATE: {year}/{month}/{day}-{hour}:{minute}'   

    smtp_server = "mail.pl"
    port = 587  # For starttls
    email_sender = "example@example.pl"
    password = "example"

    # Create a secure SSL context
    context = ssl.create_default_context()


    em = EmailMessage()
    em['From'] = email_sender
    em['BCC'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    ##########################################################

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(email_sender, password)
        # TODO: Send email here
        server.sendmail(email_sender, email_receiver, em.as_string())
        print(f'Email notification to {email_receiver} was sent!')
    except Exception:
        print('Cant send an email!')
        time.sleep(5)

    finally:
        server.quit()
        
## Start czasu trwania programu
start = time.time()


############# NETBOX API REQUEST ###################
netbox = pynetbox.api(
    'https://netbox.thehomelab.pl',
    token='token_for_netbox'
)

device_with_tag = netbox.dcim.devices.filter(tag='backup')
for device in device_with_tag:
    # Aby wyszukac dany sprzet najpierw musze zrobic z nazwy z tablicy stringa
    # po wartosci z tablicy nie wyszukuje
    device = str(device)
    # Wyszukuje sprzęty zapisane w device_with_tag po hostnamie
    device = netbox.dcim.devices.get(name=device)
    # Zapisuje IP każdego sprzętu
    ip = device.primary_ip4
    ip = str(ip)
    # Usunięcie maski z IP
    ip = ip[:-3]
    # Zapisuje Netmiko plugin jaki został przypisany do urzadzenia w Netboxie
    plugin = device.custom_fields
    plugin = plugin['Netmiko_plugin']
    # Create nested dictionary, for instance: {hostname = {'IP': 1.1.1.1, 'Netmiko plugin': 'cisco_s300'}}
    devices_to_backup[device]= {}
    devices_to_backup[device]["IP Address"] = ip
    devices_to_backup[device]["Netmiko module"] = plugin

# Do diagnozy
print(f'Pobrane urzadzenia do backupu: {devices_to_backup}')

for device in devices_to_backup:
    
    # Pobieranie wartosci zapisanych w device_to_backup
    # takich jak hostname, przypisany mu IP oraz modul Netmiko
    hostname = device
    IP = devices_to_backup[device]["IP Address"]
    Netmiko_module = devices_to_backup[device]["Netmiko module"]
    
    device = {
        'device_type': Netmiko_module,
        'host': IP,
        'username': 'username',
        'password': 'password',
        'port': 22,
        'secret': 'cisco',
        'fast_cli': False,
        'verbose': True
            }
    
    # Do starych HP używamy innego konta do logowania
    # jeżeli skrypt ma łączyc sie do nich to w locie zmieniany jest 
    # username oraz password, ta sama sytuacja pojawi sie w Juniperach
    if Netmiko_module in 'hp_comware':
            device["username"] = 'username'        #if other than first one
            device["password"] = 'password'         #if other than first one
    
    try:    
        connection = ConnectHandler(**device)
        
        if Netmiko_module == 'cisco_s300':
            connection.send_command_timing(f'copy running-config tftp://192.16.1.1/{hostname}.{year}-{month}-{day}.conf')
        
        elif Netmiko_module == 'dell_powerconnect':
            connection.send_command_timing(
                    f'copy running-config tftp://192.16.1.1/{hostname}.{year}-{month}-{day}.conf')
                  
        elif Netmiko_module == 'aruba_os':
            connection.send_command_timing(f'copy running-config tftp 192.16.1.1 {hostname}.{year}-{month}-{day}.conf')
            
        elif Netmiko_module == 'hp_procurve':
            connection.send_command_timing(f'copy running-config tftp 192.16.1.1 {hostname}.{year}-{month}-{day}.conf')

        elif Netmiko_module == 'hp_comware':
            connection.send_command_timing('_cmdline-mode on')
            connection.send_command_timing('y\n')
            connection.send_command_timing('Jinhua1920unauthorized')
            connection.send_command_timing(f'tftp 192.16.1.1 put startup.cfg {hostname}.{year}-{month}-{day}.conf')
                

        success.append(str(hostname))
        print(f'Backup for {hostname}, {IP} copied successfully. Module {Netmiko_module} has been used.')

    except(NetmikoTimeoutException):
        print(f'Backup for {hostname}, {IP} failed due to unreachable device, check connection status!')
        fail.append(str(hostname) + ":")
        fail.append('due to unreachable device.')
        amountf.append(str(hostname))
        pass

    except(AuthenticationException, NetmikoAuthenticationException):
        print(f'Backup for {hostname}, {IP} failed due to login authentication failed. Check login/password.')
        fail.append(str(hostname) + ":")
        amountf.append(str(hostname))
        fail.append('due to login authentication failed.')
        fail.append(' ')
        pass

    except:
        print(f'Unknown exception during the SSH connection to host {hostname}')
        fail.append(str(hostname) + ":")
        amountf.append(str(hostname))
        fail.append('Unknown exception during the SSH connection to host.')
        fail.append(' ')
        pass
    
amounts = success
fail =' '.join(fail)
success =', '.join(success)

########################### SPRAWDZANIE CZY PLIK BACKUP DLA DANEGO HOSTA ISTNIEJE #######################
from pathlib import Path

for device in devices_to_backup:
    hostname = device
    path_to_file = f'/backup/{hostname}.{year}-{month}-{day}.conf'
    path = Path(path_to_file)

    if path.is_file():
        print(f'The file {path_to_file} exists')
        file_exist.append(str(hostname))
    else:
        print(f'The file {path_to_file} does not exist')
        file_notexist.append(str(hostname) + ":")
        file_notexist.append(f'for day {day}/{month}/{year} was not found on the server.\n')

file_notexist =' '.join(file_notexist)
end = time.time()

########################################## EMAIL NOTIFICATION ################################################
mbmr = 'example@example.pl'
powiadomienie(f'''Succeed:[{len(amounts)}] Failed:[{len(amountf)}] Files created:[{len(file_exist)}]                                                                              
Detailed information below: 

SUCCESSFUL:     {success}

FAILED:\n     {fail}

File not exist:\n{file_notexist}

##################################
Total execution time: {end-start}
''', mbmr)

if len(amountf) > 0 or len(file_notexist) > 0:
    powiadomienie(f'''Succeed:[{len(amounts)}] Failed:[{len(amountf)}] Files created:[{len(file_exist)}] \n
Detailed information below:

SUCCESSFUL:     {success}

FAILED:\n     {fail} 

File not exist:\n{file_notexist} 

#############################
''', 'example2@example.pl')
