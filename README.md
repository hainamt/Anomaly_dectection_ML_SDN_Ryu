# Anomaly Detection for Ryu SDN Controller

![Topology](https://user-images.githubusercontent.com/84791557/132374979-7656ab1b-baab-4ead-ba1f-72405f73b5a7.png)

## Tools
- Mininet- Network Topology Simulator, can be use via Python API: http://mininet.org/download/
- Ryu SDN Controller: https://github.com/faucetsdn/ryu
- Wireshark-Packet Capture and export PCAP files: https://www.wireshark.org/download.html
- MongoDB to store Topology's information: https://www.mongodb.com/try/download/community 
- CICFlowMeter-Feature Extractor from PCAP files and export CSV files: https://github.com/ahlashkari/CICFlowMeter

## Environment setting
- Set up Shared Folder (VM VirtualBox) between Mininet Server and Controller's server
- Run Controller application from Ryu Controller: 
```
ryu-manager --observe-links --verbose Topo_to_Mongo.py ofctl_rest.py
```
- In the mininet server, use Topology/SplTp.py to build the topology and connect to the Ryu Controller:
```
sudo mn --custom SplTp.py --topo Simple_Topo --controller=remote,ip={ip address of the controller's server}
```
- Run the ML Engine from Supervisor: 
```
python StartSupervisor.py
```
- In the mininet server, run:
 - Topology/CICTrigger/CICTrigger.sh - a script with inotify tool for dectecting new PCAP files:
```
sudo ./CICTrigger.sh
```
 - Or Topology/Script PCAP to CSV/TsharkCIC.py - for the same purpose
- If using the first option, in the mininet server, run Wireshark to capture the interfaces that need to be monitored, In the mininet server, set Wireshark to run continuously at arbitrary intervals and save with "Flow.pcap".

## How it works
1. The pcap files will be saved with the format "Flow_{index}_{year}{month}{date}{hour}{minute}{second}.pcap"
2. The inotify tool in CICTrigger.sh will detect those PCAP files and automatically call the CICFlowMeter tool to convert those files into CSV Files with predefined features
3. The shared folder is used to send those CSV files directly to a repository in the Controller's server
4. Those csv files will be recognized and read by StartSupervisor.py through their index, they will be converted one last time to Dataframe and go through a trained ML model, sending out the prediction's result
5. If a source IP address is determined to be anomalous, the application will response with some actions in ManipAPI.Reaction. In this python file, 2 actions can be performed to indirectly modify flow entry of OpenFlow Switch by REST API (depending on the application running with the Controller):
 - Interact with rest_firewall
 - Interact with ofctl_rest
