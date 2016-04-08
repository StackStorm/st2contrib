from lib.icsp import ICSPBaseActions
import json


class getServerAttributes(ICSPBaseActions):
    def run(self, mids, connection_details, attribute_key, attribute_type="all"):
        if connection_details:
            self.getConnection(connection_details)
        self.getSessionID()
        endpoint = "/rest/os-deployment-servers"
        results = {}
        for mid in mids:
            try:
                id = int(mid)
            except:
                raise ValueError("MIDs must be integers")
            getreq = self.icspGET(endpoint+"/%s" % mid)
            allattr = getreq['customAttributes']
            results[mid] = allattr
            
	output = results

        # Filter based on Attribute Type 
        if not attribute_type == "all":
           filtereddata = {}
           for server in results:
               filteredelements = []
               for element in results[server]:
                   if element['values'][0]['scope'] == attribute_type:
                       filteredelements.append(element)
               filtereddata[server]= filteredelements
           output = filtereddata

        # Filter staged results to key words provided
        if attribute_key:
            filtereddata = {} 
            for server in output:
                filteredelements = []
		for element in output[server]:
                    if element['key'] == attribute_key:
                        filteredelements.append(element)
                filtereddata[server] = filteredelements
            output = filtereddata

        return {"attributes": output}
