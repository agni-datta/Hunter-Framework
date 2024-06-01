import socket

from IPy import IP
from termcolor import colored


def hunter_open_ports():
    """
    Scans for open ports on a target or multiple targets.

    Returns:
        None
    """

    def scan(target, port_range):
        """
        Scans a target for open ports.

        Args:
            target (str): IP address or domain name of the target.
            port_range (int): Range of ports to scan.

        Returns:
            None
        """
        converted_ip = check_ip(target)
        print(
            colored(
                "\n" + "[-_0]Scanning the target " + str(target),
                "yellow",
                attrs=["bold"],
            )
        )
        for port in range(1, port_range):
            scan_port(converted_ip, port)

    def check_ip(ip):
        """
        Checks if the input is an IP address or domain name and converts it if necessary.

        Args:
            ip (str): IP address or domain name.

        Returns:
            str: Converted IP address.
        """
        try:
            IP(ip)
            return ip
        except ValueError:
            return socket.gethostbyname(ip)

    def get_banner(s):
        """
        Retrieves the banner from a socket.

        Args:
            s (socket): Socket object.

        Returns:
            str: Banner message.
        """
        return s.recv(1024)

    def scan_port(ipaddress, port):
        """
        Scans a specific port on a target.

        Args:
            ipaddress (str): IP address of the target.
            port (int): Port number.

        Returns:
            None
        """
        try:
            sock = socket.socket()
            sock.settimeout(0.9)
            sock.connect((ipaddress, port))
            try:
                banner = get_banner(sock)
                print(
                    colored(
                        "[+] Open Port "
                        + str(port)
                        + " "
                        + str(banner.decode().strip("\n")),
                        "green",
                        attrs=["bold"],
                    )
                )
            except:
                print(colored("[+] Open Port " + str(port), "green", attrs=["bold"]))
        except:
            pass

    targets = input(
        "[+] Enter the Target/s to initiate Scan(Split Multiple Targets with , ): "
    )
    port_range = int(
        input("Enter the range of ports to scan(500 for first 500 ports): ")
    )
    if "," in targets:
        for ip_add in targets.split(","):
            scan(ip_add.strip(" "), port_range)
    else:
        scan(targets, port_range)
