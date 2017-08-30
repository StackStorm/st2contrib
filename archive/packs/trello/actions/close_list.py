from lib import action


class CloseListAction(action.BaseAction):
    def run(self, list_id, board_id, api_key=None, token=None):
        if api_key:
            self._set_creds(api_key=api_key, token=token)

        trello_list = self._client().get_board(board_id).get_list(list_id)
        trello_list.close()

        return trello_list.closed
