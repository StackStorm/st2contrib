import nmap

from st2actions.runners.pythonrunner import Action

"""
Note: This action requires nmap binary to be available and needs to run as root.
"""

class PortScanner(Action):

  def run(self, host):
    result = []
    port_details = {}
    ps = nmap.PortScanner()
    scan_res = ps.scan(host, arguments='--min-parallelism 100 -sT -sU -sZ')
    for target_host in ps.all_hosts():
      if target_host in ps.all_hosts():
        for comm in ps[target_host].all_protocols():
           if comm in ['tcp','udp','ip','sctp']:
             ports = ps[target_host][comm].keys()
             ports.sort()
             for port in ports:
               port_details = {port:{'state':ps[host][comm][port]['state'], 'service':ps[host][comm][port]['name'], 'protocol':comm}}
               result.append(port_details)

    return result
