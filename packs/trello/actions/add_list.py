from lib import action


class AddListAction(action.BaseAction):
    def run(self, name, board_id, api_key=None, token=None):
        if api_key:
            self._set_creds(api_key=api_key, token=token)

        new_list = self._client().get_board(board_id).add_list(name)

        if new_list:
            return new_list.id
        else:
            return False
