#!/usr/bin/env python
# Made by: @gsvprharsha(github)
# Still under development.....Feel free to contribute to this repo

import scapy.all as scapy
from pip._vendor.distlib.compat import raw_input


def hunter_network_scanner():
    """
    Scans a network for connected devices and displays their IP and MAC addresses.

    Returns:
        None
    """

    def scan(ip):
        """
        Scans the network for connected devices.

        Args:
            ip (str): IP address range to scan.

        Returns:
            list: List of dictionaries containing IP and MAC addresses.
        """
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        client_list = []
        for element in answered_list:
            client_dict = {"ip": element[1].psrc, "MAC": element[1].hwsrc}
            client_list.append(client_dict)
        return client_list

    def print_result(result_list):
        """
        Prints the result of the network scan.

        Args:
            result_list (list): List of dictionaries containing IP and MAC addresses.

        Returns:
            None
        """
        print("IP address\t\t   MAC Address\n-----------------------------------------")
        for client in result_list:
            print(client["ip"] + "\t\t" + client["MAC"])

    user_input_range = raw_input("[+] Network Range to scan for: ")
    scan_result = scan(user_input_range)
    print_result(scan_result)
