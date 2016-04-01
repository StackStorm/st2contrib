from vmwarelib.actions import BaseAction


class GetVMConsoleUrls(BaseAction):

    def run(self, vms):
        meta_url_template = 'https://{host}:{port}/vsphere-client/vmrc/vmrc.jsp?' \
                            'vm=urn:vmomi:VirtualMachine:{{vm}}:{si_uuid}'

        si_content = self.si.RetrieveContent()
        si_uuid = si_content.about.instanceUuid

        host = self.config['host']
        port = self.config['port']

        vm_url_template = meta_url_template.format(host=host, port=port, si_uuid=si_uuid)

        vm_moids = vms
        vms_console_urls = [
            {moid: {'url': vm_url_template.format(vm=moid)}} for moid in vm_moids
        ]

        return vms_console_urls
