import pyshark as ps
import time
from datetime import datetime
import subprocess
from subprocess import Popen

interfaces = ['s01-eth1','s02-eth1','s03-eth1','s01-eth2','s02-eth2','s03-eth2']
output_csv_path = '/home/natrie/Topology/OutputCSV/'
output_pcap_path = '/home/natrie/Topology/OutputPCAP/'
cicpath = './cfm'

while(True):
    now = str(datetime.now()).replace(" ","_").replace(":","-")
    filename= output_pcap_path + now + '.pcap'
    capture = ps.LiveCapture(interface=['enp0s3'],output_file=filename)
    capture.set_debug()
    capture.sniff(timeout=10)
    capture

    #command = cicpath + " " + filename + " " + output_csv_path
    #p = Popen(command,shell=True)


    