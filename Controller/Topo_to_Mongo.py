from Reaction import RESTDBconfig
from datetime import datetime
from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from ryu.topology.api import get_host

FIREWALL_URL = ''
MONGO_URL = 'mongodb://127.0.0.1:27017/'
OF_URL = 'http://localhost:8080/stats/flowentry/add'
DBName = 'SDN'
CollName = 'Topology'

class ControlTopo13(simple_switch_13.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(ControlTopo13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        self.topo_app = self
        self.device_count = 0
        try:
            self.DB = RESTDBconfig()
            self.logger.info('Connected to Database.')
        except Exception:
            self.logger.error('Cannot connect to the Database',exc_info=True)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(15)
            if self.device_count == len(self.datapaths.values()):
                self.device_count = 0
                hub.sleep(3600)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    def _to_database(self,datapathid,data, collection=CollName):
        try:
            self.logger.info('Inserting data to Database...')
            self.DB.DBconfig_update(datapathid,data,collection)
            self.logger.info('Database is updated!')
        except Exception:
            self.logger.error('Cannot insert data to the database', exc_info=True)

    def _get_hosts(self, ev_datapathid):
        
        dp = ev_datapathid

        try:
            hosts_list = get_host(self.topo_app, dpid=dp)
            host_ipv4 = [host.ipv4 for host in hosts_list]
            flattenize = [host for sublist in host_ipv4 for host in sublist]
        except Exception as ex:
            self.logger.error(ex)
        return flattenize 

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        switchs_hosts = {}
        host_all = []
        dp = ev.msg.datapath.id

        switchs_hosts['Datapath ID'] = dp
        hosts = self._get_hosts(dp)
        for host in hosts:
            dict_host = {}
            dict_host['IP'] = host
            dict_host['Status'] = 0
            host_all.append(dict_host)
        switchs_hosts['Hosts'] = host_all
        switchs_hosts['Version'] = datetime.now().strftime("%Y%m%d%H%M%S")
        
        self.device_count += 1
        #buff_info = self.device_info
        data = { "$set": switchs_hosts } 
        self._to_database(dp, data, CollName)

