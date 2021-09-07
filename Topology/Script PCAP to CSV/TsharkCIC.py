import pyshark as ps
import time
from datetime import datetime
import subprocess
from subprocess import Popen

interfaces = ['s01-eth1','s02-eth1','s03-eth1','s01-eth2','s02-eth2','s03-eth2']
output_csv_path = '/home/mininet/Topology/ICFlowMeter-4.0/bin/PCAP_to_CSV/OutputCSV/'
output_pcap_path = '/home/mininet/Topology/ICFlowMeter-4.0/bin/PCAP_to_CSV/InputPCAP/'
cicpath = 'cfm.bat'

while(True):
    now = str(datetime.now()).replace(" ","_").replace(":","-")
    filename= output_pcap_path + now + '.pcap'
    capture = ps.LiveCapture(interface=interfaces,output_file=filename)
    capture.sniff(timeout=20)
    capture

    command = cicpath + " " + filename + " " + output_csv_path
    p = Popen(command,shell=True)

    