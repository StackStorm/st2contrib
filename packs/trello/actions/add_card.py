from lib import action


class AddCardAction(action.BaseAction):
    def run(self, name, board_id, list_id, description=None, api_key=None, token=None):
        if api_key:
            self._set_creds(api_key=api_key, token=token)

        board = self._client().get_board(board_id)
        lst = board.get_list(list_id)
        card = lst.add_card(name=name, desc=description)

        if card:
            return card.id
        else:
            return False
