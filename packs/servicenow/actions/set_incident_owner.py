from lib.actions import BaseAction


class AssignIncidentToAction(BaseAction):
    def run(self, user_id, number):
        s = self.client
        s.table = 'incident'
        res = s.get({'number': number})
        sys_id = res[0]['sys_id']
        response = s.update({'assigned_to': user_id}, sys_id)
        return response
