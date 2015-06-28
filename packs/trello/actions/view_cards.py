from lib import action


class ViewCardsAction(action.BaseAction):
    def run(self, board_id, list_id, api_key=None, token=None):
        if api_key:
            self._set_creds(api_key=api_key, token=token)

        cards = {}
        board = self._client().get_board(board_id)
        lst = board.get_list(list_id)
        for card in lst.list_cards():
            cards[card.id] = {
                'name': card.name,
                'description': card.desc,
                'url': card.url,
                'closed': card.closed,
            }

        return cards
