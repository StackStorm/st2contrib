from lib import action


class ViewBoardsAction(action.BaseAction):
    def run(self, api_key=None, token=None):
        if api_key:
            self._set_creds(api_key=api_key, token=token)

        boards = {}

        for board in self._client().list_boards():
            if not board.closed:
                boards[board.id] = {
                    'name': board.name,
                    'description': board.description,
                    'closed': board.closed,
                    'url': board.url
                }

        return boards
