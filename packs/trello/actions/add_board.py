from lib import action


class AddBoardAction(action.BaseAction):
    def run(self, name, api_key=None, token=None):
        if api_key:
            self._set_creds(api_key=api_key, token=token)

        new_board = self._client().add_board(name)
        return new_board.id if new_board else False
