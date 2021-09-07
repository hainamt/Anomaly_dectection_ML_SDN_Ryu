import requests as rq
from pymongo import MongoClient

FIREWALL_URL = ' http://localhost:8080/firewall/'
MONGO_URL = 'mongodb://127.0.0.1:27017/'
OF_URL = 'http://localhost:8080/stats/'
DBName = 'SDN'
CollName = 'Topology'

class RESTFWconfig(object):
    def __init__(self, fw_url=FIREWALL_URL):
        """
        Start the Firewall and allow all Switchs to convey
        """
        self.fw_enable_url = fw_url + 'module/enable/' 
        self.fw_rule_url = fw_url + 'rules/'
        rq.put(self.fw_enable_url + "all")
        #rq.post(self.fw_rule_url + "all")
        rq.delete(self.fw_rule_url + "all", data='{"rule_id": "all"}')

    def get_rules(self, datapathid):
        rq_rules = rq.get(self.fw_rule_url + f"{datapathid:016d}")
        return rq_rules.content

    def FWconfig_add_rule(self,ip_src, datapathid, action):
        """
        Action can be operated: ALLOW, DENY
        """
        rule = '{{"nw_src": {ip_source} , "actions": {action}}}'.format(ip_source = ip_src + "/32", action=action)
        rq.post(self.fw_rule_url + f"{datapathid:016d}", data=rule)

    def FWconfig_del(self, datapathid,rule_id):
        rq.delete(self.fw_rule_url + f"{datapathid:016d}", data='{{"rule_id": {id}}}'.format(id = rule_id))

class RESTOFconfig(object):
    """
    Manipulate with OpenFlow via REST API
    """
    def __init__(self, of_url=OF_URL):
        self.desc_url = of_url + "desc/"
        self.flow_url = of_url + "flow/"
        self.port_url = of_url + "port/"
        self.flowentry_url = of_url + "flowentry/"

    def get_sw_stt(self, datapathid):
        rq_sw_stt = rq.get(self.desc_url+str(datapathid))
        return rq_sw_stt.content

    def get_flow_stt(self,datapathid):
        rq_flow_stt = rq.get(self.flow_url+str(datapathid))
        return rq_flow_stt.content

    def get_port_stt(self,datapathid, port = None):
        if port == None:
            rq_port_stt = rq.get(self.port_url + str(datapathid))
        else:
            rq_port_stt = rq.get(self.port_url + str(datapathid)+'/'+str(port))
        return rq_port_stt.content
    
    def block_entry(self, datapathid, ip_src, priority=11111, time=1800):
        entry = """{{"dpid": {dapaid}, "table_id": 0, "idle_timeout": "{time_out}", "hard_timeout": "{time_out}", 
                "match": {{"ipv4_src": "{IP_src}", "eth_type": 2048}}, "priority": {Priority}, 
                "actions": [{{ "type": "CLEAR_ACTIONS"}}]}}""".format(dapaid=datapathid, IP_src=ip_src,time_out=time, Priority=priority)
        rq_entry_drop = rq.post(self.flowentry_url + "add",data=entry)
        return rq_entry_drop.content
    
    def open_entry(self, datapathid,ip_src, priority=11111, time=1800):
        match_cond = """{{"dpid": {dapaid}, "table_id": 0, "idle_timeout": {time_out}, "hard_timeout": {time_out}, 
                    "match": {{"ipv4_src": "{IP_src}", "eth_type": 2048}}, "priority": {Priority}, 
                    "actions": [{{ "type": "CLEAR_ACTIONS"}}]}}""".format(dapaid=datapathid, IP_src=ip_src,time_out = time ,Priority=priority)
        rq_open = rq.post(self.flowentry_url + "delete", data=match_cond)
        return rq_open.content

class RESTDBconfig(object):
    """
    Initiate connection with MongoDB and perform some actions
    """
    def __init__(self, db_url=MONGO_URL,db_name=DBName):
        self.db = MongoClient(db_url)[db_name]

    def DBconfig_update(self,datapathid,data,collection_name=CollName):
            filter = {'Datapath ID' : datapathid}
            self.db[collection_name].update_one(filter, data, upsert=True)

    def DBconfig_update_status(self, ip_src, increase=5, collection_name=CollName):
        self.db[collection_name].update_one({"Hosts.IP": ip_src}, {'$inc':{"Hosts.$.Status": increase}})

    def DBconfig_query(self, ip_src, collection_name=CollName):
        self.db[collection_name].find({})
        query = list(self.db[collection_name].find({ 'Hosts' : { '$elemMatch': { 'IP': ip_src } } }, {'_id': False, 'Version': False}))
        for host in query[0]['Hosts']:
            if host['IP'] == ip_src:
                stt = host['Status']
        dp = query[0]['Datapath ID']
        return dp, stt

    def DBConfig_del(self, datapathid,collection_name=CollName):
        self.db[collection_name].delete_one({'$elemMatch' : {'DatapathID':datapathid}})
