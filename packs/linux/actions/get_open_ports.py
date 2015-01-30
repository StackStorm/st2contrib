import nmap

from st2actions.runners.pythonrunner import Action

"""
Note 1: This action requires nmap binary to be available.

Note 2: We only scan for open TCP ports since scanning for open UDP ports
                (-sU) requires root priveleges.
"""


class PortScanner(Action):
    def run(self, host):
        result = []
        port_details = {}
        ps = nmap.PortScanner()
        ps.scan(host, arguments='--min-parallelism 100 -sT')
        for target_host in ps.all_hosts():
            if target_host not in ps.all_hosts():
                continue

            for comm in ps[target_host].all_protocols():
                if comm in ['tcp', 'udp', 'ip', 'sctp']:
                    ports = ps[target_host][comm].keys()
                    ports.sort()
                    for port in ports:
                        port_details = {
                            port: {
                                'state': ps[host][comm][port]['state'],
                                'service': ps[host][comm][port]['name'],
                                'protocol': comm
                            }
                        }
                        result.append(port_details)

        return result
