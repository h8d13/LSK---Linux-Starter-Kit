from scapy.all import sniff, TCP

def process_packet(packet):
    if packet.haslayer(TCP):
        print(packet[TCP].show())

sniff(prn=process_packet)

## This script will sniff all TCP packets
# Needs to run with SUDO and have pip install scapy in your .venv
