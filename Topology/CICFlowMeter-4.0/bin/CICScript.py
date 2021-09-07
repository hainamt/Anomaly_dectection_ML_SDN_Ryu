import subprocess
from subprocess import Popen

cicpath = 'cfm.bat'
inputpath = 'PCAP_to_CSV\InputPCAP'
outputpath = 'PCAP_to_CSV\OutputCSV'
command = cicpath + " " + inputpath + " " + outputpath

p = Popen(command,shell=True)