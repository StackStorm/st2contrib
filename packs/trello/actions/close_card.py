from lib import action

class CloseCardAction(action.BaseAction):
    def run(self, card_id, api_key=None, api_secret=None, token=None, token_secret=None):
        if api_key:
            self._set_creds(api_key=api_key, api_secret=api_secret,
                             token=token, token_secret=token_secret)

        card = self._client.get_card(card_id)
        card.set_closed()

        return card.closed


