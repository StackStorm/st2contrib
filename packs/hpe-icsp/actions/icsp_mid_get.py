from lib import checkinputs
from lib.icsp import ICSPBaseActions


class GetMid(ICSPBaseActions):
    def run(self, uuid, serialnumber, connection_details):
        checkinputs.one_of_two_strings(uuid, serialnumber, "UUID or SerialNumber")
        if connection_details:
            self.setConnection(connection_details)
        self.getSessionID()
        endpoint = "/rest/os-deployment-servers"
        results = self.icspGET(endpoint)
        servers = results["members"]
        for server in servers:
            if (server["uuid"] == uuid) or\
                    (server["serialNumber"] == serialnumber):
                mid = server["mid"]
                continue

        return {'mid': mid}
