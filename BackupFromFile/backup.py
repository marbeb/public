from netmiko import ConnectHandler

class Device:
    def __init__(self, ip: str, netmiko_module: str):
        self.ip = ip
        self.netmiko_module = netmiko_module

    def createBackup(self, username: str, password: str, secret = None, port = 22, fast_cli = False, verbose = True):
        try:
            print(f'Connecting to {self.ip} using {self.netmiko_module}.')
            connection = ConnectHandler({
                'device_type': self.netmiko_module,
                'host': self.ip,
                'username': username,
                'password': password,
                'port': port,
                'secret': secret and secret or '',
                'fast_cli': fast_cli,
                'verbose': verbose
            })
            connection.send_command_timing(f'copy running-config tftp://172.16.150.10/backup.conf')
        except:
            print(f'Cannot connect to {self.ip}.')

    @staticmethod
    def createBackupByFile(file: str, netmiko_module: str, username: str, password: str, secret = None, port = 22, fast_cli = False, verbose = True):
        with open(file, 'r') as file:
            content = file.read()
            ips = content.splitlines()

        for ip in ips:
            device = Device(ip, netmiko_module)
            device.createBackup(username, password, port, secret, fast_cli, verbose)



Device.createBackupByFile('devices.txt', 'netmiko_module', 'login', 'password', 'cisco')




