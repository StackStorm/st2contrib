from lib import action


class Action(action.BaseAction):
    def run(self, board_id, api_key=None, token=None):
        if api_key:
            self._set_creds(api_key=api_key, token=token)

        lists = {}
        board = self._client().get_board(board_id)
        for lst in board.all_lists():
            lists[lst.id] = {
                'name': lst.name,
                'closed': lst.closed
            }

        return lists
