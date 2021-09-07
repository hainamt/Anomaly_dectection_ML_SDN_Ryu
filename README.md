# Anomaly Detection for Ryu SDN Controller

![Untitled](https://user-images.githubusercontent.com/84791557/128701358-cdd2805d-085f-4e57-b9e4-bf97cd52d787.png)

## Tools
- Mininet- Network Topology Simulator, available via Python API: http://mininet.org/download/
- Ryu SDN Controller: https://github.com/faucetsdn/ryu
- Wireshark-Packet Capture and export PCAP files: https://www.wireshark.org/download.html
- CICFlowMeter-Feature Extractor from PCAP files and export CSV files: https://github.com/ahlashkari/CICFlowMeter

## Environment setting
- Set up Shared Folder between Mininet Server and Controller's server
- Run Controller application from Ryu Controller (simple_switch_13.py, simple_monitor_13.py, ...)
- Run the ML Engine from Supervisor/StartSupervisor.py
- In the mininet server, use Topology/SplTp.py to build the topology and connect to the Ryu Controller:
```
sudo mn --custom SplTp.py --topo Simple_Topo --controller=remote,ip={ip address of the controller's server}
```
- In the mininet server, run:
 - Topology/CICTrigger/CICTrigger.sh - a script with inotify tool for dectecting new PCAP files
 - Or Topology/Script PCAP to CSV/TsharkCIC.py - for the same purpose
- If using the first option, in the mininet server, run Wireshark to capture the interfaces that need to be monitored, In the mininet server, set Wireshark to run continuously at arbitrary intervals and save with "Flow.pcap".

## How it works
- The pcap files will be saved with the format "Flow_{index}_{year}{month}{date}{hour}{minute}{second}.pcap"
- The inotify tool in CICTrigger.sh will detect those PCAP files and automatically call the CICFlowMeter tool to convert those files into CSV Files with predefined features
- The shared folder is used to send those CSV files directly to a repository in the Controller's server
- Those csv files will be recognized and read by StartSupervisor.py through their index, they will be converted one last time to Dataframe and go through a trained ML model, sending out the prediction's result
- If a source IP address is determined to be anomalous, various responses can be taken (not mentioned in the source code), for example interacting with a firewall or with the OpenFlow protocol.
- **(Optional)** Run OpenFlow REST API application from Ryu Controller - for the purpose of interacting with Openflow
- **(Optional)** Run MongoDB application - for the purpose of storing Topology's Data, Controller's Data, Application's Data
