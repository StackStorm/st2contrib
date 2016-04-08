from lib.icsp import ICSPBaseActions
import json


class setServerAttributes(ICSPBaseActions):
    def run(self, mid, connection_details, attributes, function):
        if connection_details:
            self.setConnection(connection_details)
        self.getSessionID()
        endpoint = "/rest/os-deployment-servers/%s" % mid
        payload = {"category": "os-deployment-servers",
                   "customAttributes": [], "type": "OSDServer"}
        for attribute in attributes:
            payload["customAttributes"].append(
                {"key": attribute, "values": [
                    {"scope": "server", "value": attributes[attribute]}]})

        # If function is set to append any undefined attributes from server
        # any attribute to replace must be defined in full in the new call 

        if function == "append":
            currentdetails = self.icspGET(endpoint)
            for element in currentdetails['customAttributes']:
                if element['values'][0]['scope'] == 'server'\
                    and not element['key'].startswith("__"):
                        oldatt = {"key": element['key'], "values": [
                            {"scope": "server", 
                             "value": element['values'][0]['value']}]}
                        if not oldatt in payload['customAttributes']:
                            payload['customAttributes'].append(oldatt)

        try:
            self.icspPUT(endpoint, payload)
        except Exception as e:
            raise Exception("Error: %s" % e)
        return
