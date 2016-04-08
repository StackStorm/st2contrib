from lib.icsp import ICSPBaseActions


class GetBuildPlans(ICSPBaseActions):
    def run(self, plan_names, connection_details):
        if connection_details:
            self.setConnection(connection_details)
        self.getSessionID()

        endpoint = "/rest/os-deployment-build-plans"
        results = self.icspGET(endpoint)
        plans = []
        for plan in results["members"]:
            if plan_names:
                for name in plan_names:
                    if name.lower() == str(plan["name"]).lower():
                        uri = plan["uri"].split("/")[-1]
                        plans.append({"name": plan["name"], "uri": uri})
            else:
                uri = plan["uri"].split("/")[-1]
                plans.append({"name": plan["name"], "uri": uri})

        return {"plans": plans}
