from lib import action


class FindCardByNameAction(action.BaseAction):
    def run(self, name, board_id, list_id, api_key=None, token=None):
        if api_key:
            self._set_creds(api_key=api_key, token=token)

        cards = []
        board = self._client().get_board(board_id)
        lst = board.get_list(list_id)

        for card in lst.list_cards():
            if card.name == name and not card.closed:
                cards.append(card.id)

        if len(cards) == 0:
            return False
        else:
            return cards
