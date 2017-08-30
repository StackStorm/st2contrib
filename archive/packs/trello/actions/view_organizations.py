from lib import action


class ViewOrganizationsAction(action.BaseAction):
    def run(self, api_key=None, token=None):
        if api_key:
            self._set_creds(api_key=api_key, token=token)

        orgs = {}
        for org in self._client.list_organizations():
            orgs[org.id] = org.name

        return orgs
