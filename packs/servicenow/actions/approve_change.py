from lib.actions import BaseAction


class ApprovalAction(BaseAction):
    def run(self, number):
        s = self.client
        s.table='change_request'
        res = s.get({'number': number})
        sys_id = res[0]['sys_id']
        response = s.update({'approval': 'approved'}, sys_id) 
        return response
