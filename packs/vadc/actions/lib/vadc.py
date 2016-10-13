#!/usr/bin/python

import requests
import sys
import json


class Vadc:

    DEBUG = False

    def __init__(self, host, user, passwd, logger):
        requests.packages.urllib3.disable_warnings()
        self.host = host
        self.user = user
        self.passwd = passwd
        self.logger = logger
        self.client = None

    def _debug(self, message):
        if Vadc.DEBUG:
            self.logger.debug(message)

    def _initHTTP(self):
        self.client = requests.Session()
        self.client.auth = (self.user, self.passwd)

    def _getConfig(self, url):
        self._debug("URL: " + url)
        try:
            self._initHTTP()
            response = self.client.get(url, verify=False)
        except:
            self.logger.error("Error: Unable to connect to API")
            raise Exception("Error: Unable to connect to API")
        self._debug("Status: {}".format(response.status_code))
        self._debug("Body: " + response.text)
        return response

    def _pushConfig(self, url, config, method="PUT", ct="application/json"):
        self._debug("URL: " + url)
        try:
            self._initHTTP()
            config = json.dumps(config)
            if method == "PUT":
                response = self.client.put(url, verify=False, data=config,
                    headers={"Content-Type": ct})
            else:
                response = self.client.post(url, verify=False, data=config,
                    headers={"Content-Type": ct})
        except requests.exceptions.ConnectionError:
            self.logger.error("Error: Unable to connect to API")
            raise Exception("Error: Unable to connect to API")

        self._debug("DATA: " + config)
        self._debug("Status: {}".format(response.status_code))
        self._debug("Body: " + response.text)
        return response

    def _delConfig(self, url):
        self._debug("URL: " + url)
        try:
            self._initHTTP()
            response = self.client.delete(url, verify=False)
        except requests.exceptions.ConnectionError:
            sys.stderr.write("Error: Unable to connect to API {}".format(url))
            raise Exception("Error: Unable to connect to API")

        self._debug("Status: {}".format(response.status_code))
        self._debug("Body: " + response.text)
        return response

    def _dictify(self, listing, keyName):
        dictionary = {}
        for item in listing:
            k = item.pop(keyName)
            dictionary[k] = item


class Bsd(Vadc):

    def __init__(self, config, logger):

        try:
            host = config['brcd_sd_host']
            user = config['brcd_sd_user']
            passwd = config['brcd_sd_pass']
        except KeyError:
            raise ValueError("brcd_sd_host, brcd_sd_user, and brcd_sd_pass must be configured")

        Vadc.__init__(self, host, user, passwd, logger)
        if host.endswith('/') == False:
            host += "/"
        self.baseUrl = host + "api/tmcm/2.2"

    def addVtm(self, vtm, password, address, bw, fp):
        url = self.baseUrl + "/instance/?managed=false"

        if address is None:
            address = vtm

        config = {"bandwidth": bw, "tag": vtm, "owner": "stanley", "stm_feature_pack": fp,
            "rest_address": address + ":9070", "admin_username": "admin", "rest_enabled": False,
            "host_name": address, "management_address": address}

        if password is not None:
            config["admin_password"] = password
            config["rest_enabled"] = True
            config["license_name"] = "universal_v3"

        res = self._pushConfig(url, config, "POST")
        if res.status_code != 201:
            raise Exception("Failed to add vTM. Response: {}, {}".format(res.status_code, res.text))
        return res.json()

    def delVtm(self, vtm):
        url = self.baseUrl + "/instance/" + vtm
        config = {"status": "deleted"}
        res = self._pushConfig(url, config, "POST")
        if res.status_code != 200:
            raise Exception("Failed to del vTM. Response: {}, {}".format(res.status_code, res.text))
        return res.json()

    def listVtms(self, full, deleted, stringify):
        url = self.baseUrl + "/instance/"
        res = self._getConfig(url)
        if res.status_code != 200:
            raise Exception("Failed to list. Response: {}, {}".format(res.status_code, res.text))

        output = []
        instances = res.json()
        for instance in instances["children"]:
            current = self._getConfig(url + instance["name"])
            config = current.json()
            if deleted is False and config["status"] == "Deleted":
                continue
            if full:
                config["name"] = instance["name"]
                output.append(config)
            else:
                out_dict = {k: config[k] for k in ("host_name", "tag", "status",
                    "stm_feature_pack", "bandwidth")}
                out_dict["name"] = instance["name"]
                output.append(out_dict)

        if stringify:
            return json.dumps(output, encoding="utf-8")
        else:
            return output

    def getStatus(self, vtm=None, stringify=False):
        url = self.baseUrl + "/monitoring/instance"
        res = self._getConfig(url)
        if res.status_code != 200:
            raise Exception("Failed get Status. Result: {}, {}".format(res.status_code, res.text))

        instances = res.json()
        if vtm is not None:
            for instance in instances:
                if instance["tag"] != vtm and instance["name"] != vtm:
                    instances.remove(instance)

        if stringify:
            return json.dumps(instances, encoding="utf-8")
        else:
            return instances

    def getErrors(self, stringify=False):
        instances = self.getStatus()
        errors = {}
        for instance in instances:
            error = {}
            self._debug(instance)
            if instance["id_health"]["alert_level"] != 1:
                error["id_health"] = instance["id_health"]
            if instance["rest_access"]["alert_level"] != 1:
                error["rest_access"] = instance["rest_access"]
            if instance["licensing_activity"]["alert_level"] != 1:
                error["licensing_activity"] = instance["licensing_activity"]
            if instance["traffic_health"]["error_level"] != "ok":
                error["traffic_health"] = instance["traffic_health"]
            if len(error) != 0:
                error["tag"] = instance["tag"]
                error["name"] = instance["name"]
                if "traffic_health" in error:
                    if "virtual_servers" in error["traffic_health"]:
                        del error["traffic_health"]["virtual_servers"]
                errors[instance["name"]] = error

        if stringify:
            return json.dumps(errors, encoding="utf-8")
        else:
            return errors


class Vtm(Vadc):

    def __init__(self, config, logger, vtm):

        try:
            self._proxy = config['brcd_sd_proxy']
            if self._proxy:
                host = config['brcd_sd_host']
                user = config['brcd_sd_user']
                passwd = config['brcd_sd_pass']
            else:
                host = config['brcd_vtm_host']
                user = config['brcd_vtm_user']
                passwd = config['brcd_vtm_pass']
        except KeyError:
            raise ValueError("You must set key brcd_sd_proxy, and either " +
                "brcd_sd_[host|user|pass] or brcd_vtm_[host|user|pass].")

        Vadc.__init__(self, host, user, passwd, logger)
        if host.endswith('/') == False:
            host += "/"
        if self._proxy:
            self.baseUrl = host + "api/tmcm/2.2/instance/{}/tm/3.8/config/active".format(vtm)
        else:
            self.baseUrl = host + "api/tm/3.8/config/active"

    def _getNodeTable(self, name):
        url = self.baseUrl + "/pools/" + name
        res = self._getConfig(url)
        if res.status_code != 200:
            raise Exception("Failed to get pool. Result: {}, {}".format(res.status_code, res.text))

        config = res.json()
        return config["properties"]["basic"]["nodes_table"]

    def _getVSConfig(self, name):
        url = self.baseUrl + "/virtual_servers/" + name
        res = self._getConfig(url)
        if res.status_code != 200:
            raise Exception("Failed to get VS. Result: {}, {}".format(res.status_code, res.text))

        config = res.json()
        return config

    def _setVSConfig(self, name, config):
        url = self.baseUrl + "/virtual_servers/" + name
        res = self._pushConfig(url, config)
        if res.status_code != 200:
            raise Exception("Failed to set VS. Result: {}, {}".format(res.status_code, res.text))
        config = res.json()
        return config

    def _getVSRules(self, name):
        config = self._getVSConfig(name)
        rules = {k: config["properties"]["basic"][k] for k in
                ("request_rules", "response_rules", "completionrules")}
        return rules

    def _setVSRules(self, name, rules):
        config = {"properties": {"basic": rules}}
        res = self._setVSConfig(name, config)
        if res.status_code != 200:
            raise Exception("Failed set VS Rules. Result: {}, {}".format(res.status_code, res.text))

    def enableMaintenance(self, vsname, rulename, enable=True):
        rules = self._getVSRules(vsname)
        if enable:
            if rulename in rules["request_rules"]:
                raise Exception("VServer {} already in maintenance".format(vsname))
            rules["request_rules"].insert(0, rulename)
        else:
            if rulename not in rules["request_rules"]:
                raise Exception("VServer {} is not in maintenance".format(vsname))
            rules["request_rules"].remove(rulename)
        self._setVSRules(vsname, rules)

    def getPoolNodes(self, name):
        nodeTable = self._getNodeTable(name)
        nodes = {"active": [], "disabled": [], "draining": []}
        for node in nodeTable:
            if node["state"] == "active":
                nodes["active"].append(node["node"])
            elif node["state"] == "disabled":
                nodes["disabled"].append(node["node"])
            elif node["state"] == "draining":
                nodes["draining"].append(node["node"])
            else:
                self.logger.warn("Unknown Node State: {}".format(node["state"]))

        return nodes

    def drainNodes(self, name, nodes, drain=True):
        url = self.baseUrl + "/pools/" + name
        nodeTable = self._getNodeTable(name)
        for entry in nodeTable:
            if entry["node"] in nodes:
                if drain:
                    entry["state"] = "draining"
                else:
                    entry["state"] = "active"

        config = {"properties": {"basic": {"nodes_table": nodeTable}}}
        res = self._pushConfig(url, config)
        if res.status_code != 201 and res.status_code != 200:
            raise Exception("Failed to add pool. Result: {}, {}".format(res.status_code, res.text))

    def addPool(self, name, nodes, algorithm):
        url = self.baseUrl + "/pools/" + name

        nodeTable = []
        for node in nodes:
            nodeTable.append({"node": node, "state": "active"})

        config = {"properties": {"basic": {"nodes_table": nodeTable, "monitors": ["Ping"]},
            "load_balancing": {"algorithm": algorithm}}}

        res = self._pushConfig(url, config)
        if res.status_code != 201 and res.status_code != 200:
            raise Exception("Failed to add pool. Result: {}, {}".format(res.status_code, res.text))

    def delPool(self, name):
        url = self.baseUrl + "/pools/" + name
        res = self._delConfig(url)
        if res.status_code != 204:
            raise Exception("Failed to del pool. Result: {}, {}".format(res.status_code, res.text))

    def addVserver(self, name, pool, tip):
        url = self.baseUrl + "/virtual_servers/" + name
        config = {"properties": {"basic": {"pool": pool, "port": 80, "protocol": "http",
            "listen_on_any": False, "listen_on_traffic_ips": [tip], "enabled": True}}}

        res = self._pushConfig(url, config)
        if res.status_code != 201:
            raise Exception("Failed to add VS. Result: {}, {}".format(res.status_code, res.text))

    def delVserver(self, name):
        url = self.baseUrl + "/virtual_servers/" + name
        res = self._delConfig(url)
        if res.status_code != 204:
            raise Exception("Failed to del VS. Result: {}, {}".format(res.status_code, res.text))

    def addTip(self, name, vtms, addresses):
        url = self.baseUrl + "/traffic_ip_groups/" + name

        config = {"properties": {"basic": {"ipaddresses": addresses,
            "machines": vtms, "enabled": True}}}

        res = self._pushConfig(url, config)
        if res.status_code != 201:
            raise Exception("Failed to add TIP. Result: {}, {}".format(res.status_code, res.text))

    def delTip(self, name):
        url = self.baseUrl + "/traffic_ip_groups/" + name
        res = self._delConfig(url)
        if res.status_code != 204:
            raise Exception("Failed to del TIP. Result: {}, {}".format(res.status_code, res.text))
