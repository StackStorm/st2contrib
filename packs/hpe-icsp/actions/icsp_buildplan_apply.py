from lib.icsp import ICSPBaseActions
import json


class Apply(ICSPBaseActions):
    def run(self, buildplan_uris, server_data, connection_details):
        if connection_details:
            self.setConnection(connection_details)
        self.getSessionID()

        # Prepare Endpoint within ICSP API
        endpoint = "/rest/os-deployment-jobs"

        # Prepare Pesonality Data data collection
	pload = {}
        pload['osbpUris'] = []
        pload['failMode'] = None
        pload['serverData'] = []

        for plan in buildplan_uris:
            # Confirm input are integers
            try:
            	check = int(plan)
            except:
                raise ValueError("Build plans must be Integers (comma seperated)")
       
            pload["osbpUris"].append("/rest/os-deployment-build-plans/%s" % plan)

        for server in server_data:
            data = {}
            pdata = {}
            data['serverUri'] = "/rest/os-deployment-servers/%s" % server

            # Prepare server personality Data
            # Initially not including network data Although this can be included later

            if "hostname" in server_data[server]:
                pdata['hostName'] = server_data[server]['hostname']
            if "domain" in server_data[server]:
                pdata['domain'] = server_data[server]['domain']
            if "workgroup" in server_data[server]:
                pdata['workgroup'] = server_data[server]['workgroup']
            data['personalityData'] = pdata

            pload['serverData'].append(data)

        payload = json.dumps(pload)
        try:
            results = self.icspPOST(endpoint, payload)
        except Exception as e:
            raise Exception("Error: %s" % e)

        return {"jobid": results['uri'].rsplit("/")[-1]}
