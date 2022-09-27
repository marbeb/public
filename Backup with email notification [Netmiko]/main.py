#############################
# BY linkedin.com/in/marbeb #
##############################
import time
from email.message import EmailMessage
import smtplib
import ssl
from netmiko import ConnectHandler
from datetime import datetime
from paramiko.ssh_exception import AuthenticationException
from netmiko import NetmikoTimeoutException
from netmiko import NetmikoAuthenticationException
import sys

devices_hostname = []
fail = []
success = []
amountf = []

now = datetime.now()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute

devices = ['10.101.1.2', '10.101.1.3', '10.101.1.4']

for IP in devices:
    device = {
            'device_type': 'cisco_ios',
            'host': IP,
            'username': 'admin',
            'password': 'admin',
            'port': 22,
            'secret': 'cisco',
            'verbose': True
            }
    try:
        connection = ConnectHandler(**device)
        output = connection.send_command('show running-config')
        output = output[61:]
        prompt = connection.find_prompt()

        ######SPRAWDZANIE HOSTNAME######
        hostname = prompt[:-1]
        devices_hostname.append(hostname)
        device_hostname = ', '.join(devices_hostname)

        if minute < 10:
            file_name = f"{hostname}-{year}-{month}-{day}-[{hour};0{minute}].txt"
        else:
            file_name = f"{hostname}-{year}-{month}-{day}-[{hour};{minute}].txt"

        with open(file_name, 'w') as f:
            f.write(output)
            print(30 * '#')
            print(f'Backup of {hostname} completed!')
            print(30 * '#')

        success.append(IP)
        connection.disconnect()

    except(NetmikoTimeoutException):
        print(f'Backup for {device["host"]} failed due to unreachable device, check connection status!')
        fail.append(IP)
        fail.append(':')
        fail.append('due to unreachable device.')
        amountf.append(IP)

        pass

    #JAK LOGIN FAILED TO NORMALNIE WYWALA SKRYPT - DZIEKI TEMU COS ROBI ZANIM SIE WYWALI
    except(AuthenticationException, NetmikoAuthenticationException):
        fail.append(IP)
        fail.append(':')
        fail.append('due to login authentication failed.')
        fail.append(' ')
        amountf.append(IP)
        print(30 * '#')
        print(f'Backup for {device["host"]} failed due to login authentication failed. Check login/password.')
        print(30 * '#')
        pass

#############DANE MAILA############################
email_sender = 'xxx@gmail.com'
email_password = 'code_from_gmail'
email_receiver = 'yyy@gmail.com'

amounts = success

fail =' '.join(fail)
success =', '.join(success)

#EMAIL NOTIFICATION
#TITLE AND DECCRIPTION OF AN EMAIL
if minute < 10:
    subject = f'S[{len(amounts)}]/F[{len(amountf)}] Backup notification status DATE: {day}/{month}/{year}-{hour}:0{minute}'
else:
    subject = f'S[{len(amounts)}]/F[{len(amountf)}] Backup notification status DATE: {day}/{month}/{year}-{hour}:{minute}'

body = f'''BACKUP NOTIFICATION STATUS                                                                                  
Your script created backup:  

SUCCESSFUL:     {success}

FAILED:     {fail}

#######################################

by marcin.bebenek
'''

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

##########WYSYLANIE MAILA###############
context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        #na dole hash bo jak jest jeden mail w liscie to kiepsko formatuje tekst
        #email_receiver = ', '.join(email_receiver)
        print(f'Email notification to {email_receiver} was sent!')
        print(f'Script by linkedin.com/in/marbeb')

time.sleep(3)