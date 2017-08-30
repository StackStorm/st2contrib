import dateutil.parser
from trello import TrelloClient
from st2reactor.sensor.base import PollingSensor


class TrelloListSensor(PollingSensor):
    """
    Sensor which monitors Trello list for a new actions (events).

    For reference see Trello API Docs:
    https://trello.com/docs/api/list/index.html#get-1-lists-idlist-actions
    """
    TRIGGER = 'trello.new_action'

    def __init__(self, sensor_service, config=None, poll_interval=None):
        """
        Set defaults and validate YAML config metadata.
        """
        super(TrelloListSensor, self).__init__(sensor_service, config, poll_interval)
        self._logger = self._sensor_service.get_logger(__name__)

        list_actions_sensor = self._config.get('list_actions_sensor')
        if not list_actions_sensor:
            raise ValueError('[TrelloListSensor]: "list_sensor" config value is required!')

        self._lists = list_actions_sensor.get('lists', [])
        if not self._lists:
            raise ValueError('[TrelloListSensor]'
                             '"lists" config value should have at least one entry!')

    def setup(self):
        """
        Run the sensor initialization / setup code (if any).
        """
        pass

    def poll(self):
        """
        Iterate through all Trello lists from sensor config.
        Fetch latest actions for each Trello List, filter by type.
        Start reading feed where we stopped last time
        by passing `since` date parameter to Trello API.
        Save latest event `date` in st2 key-value storage for each Trello list.
        """
        self._logger.debug('[TrelloListSensor]: Entering into listen mode ...')
        for trello_list_config in self._lists:
            self._update_credentials_by_precedence(trello_list_config)

            l = TrelloList(**trello_list_config)
            self._logger.debug("[TrelloListSensor]: Processing queue for Trello list: '%s'"
                           % l.list_id)

            actions = l.fetch_actions(
                filter=trello_list_config.get('filter') or None,
                since=self._sensor_service.get_value(l.key_name)
            )

            for action in reversed(actions):
                self._logger.debug("[TrelloListSensor]: Found new action for Trello list: '%r'"
                           % action)
                self._sensor_service.dispatch(trigger=self.TRIGGER, payload=action)
                if is_date(action.get('date')):
                    self._sensor_service.set_value(l.key_name, action.get('date'))

    def _update_credentials_by_precedence(self, trello_list_config):
        """
        Find Trello API credentials (`api_token` and `token`) from config.
        Precedence:
            1. First try to find `api_key` (list config)
            2. If not found - go to parent level (config for all lists)
            3. If not found - go to parent level (global config)
        It means that every Trello list can have its own unique API credentials to login.

        :param trello_list_config: Configuration for single Trello list
        :type trello_list_config: ``dict``

        :rtype: ``None``
        """
        if not trello_list_config.get('api_key'):
            found_credentials = self._config['list_actions_sensor']\
                if self._config['list_actions_sensor'].get('api_key') else self._config

            trello_list_config['api_key'] = found_credentials.get('api_key')
            trello_list_config['token'] = found_credentials.get('token')

    def cleanup(self):
        """
        Run the sensor cleanup code (if any).
        """
        pass

    def add_trigger(self, trigger):
        """
        Runs when trigger is created
        """
        pass

    def update_trigger(self, trigger):
        """
        Runs when trigger is updated
        """
        pass

    def remove_trigger(self, trigger):
        """
        Runs when trigger is deleted
        """
        pass


class TrelloList(object):
    """
    Sugar class to work with Trello Lists.
    """
    def __init__(self, board_id, list_id, api_key, token=None, **kwargs):
        """
        Validate inputs and connect to Trello API.
        Exception is thrown if input details are not correct.

        :param board_id: Trello board ID where the List is located
        :type board_id: ``str``

        :param list_id: Trello List ID itself
        :type list_id: ``str``

        :param api_key: Trello API key
        :type api_key: ``str``

        :param token: Trello API token
        :type token: ``str``
        """
        self.board_id = board_id
        self.list_id = list_id
        self.api_key = api_key
        # assume empty string '' as None
        self.token = token or None

        self.validate()

        self._client = TrelloClient(api_key=self.api_key, token=self.token)
        self._list = self._client.get_board(self.board_id).get_list(self.list_id)

    def validate(self):
        """
        Ensure that Trello list details are correct.
        Raise an exception if validation failed.
        """
        if not self.api_key:
            raise ValueError('[TrelloListSensor] "api_key" config value is required!')
        assert isinstance(self.api_key, basestring)

        if self.token:
            assert isinstance(self.token, basestring)

        if not self.board_id:
            raise ValueError('[TrelloListSensor]: "board_id" config value is required!')
        assert isinstance(self.board_id, basestring)

        if not self.list_id:
            raise ValueError('[TrelloListSensor]: "list_id" config value is required!')
        assert isinstance(self.list_id, basestring)

    @property
    def key_name(self):
        """
        Generate unique key name for built-in storage based on config values.

        :rtype: ``str``
        """
        return '{}.{}.date'.format(self.board_id, self.list_id)

    def fetch_actions(self, filter=None, since=None):
        """
        Fetch actions for Trello List with possibility to specify filters.
        Example API request:
        https://api.trello.com/1/lists/{list_id}/actions?filter=createCard&since=2015-09-14T21:45:56.850Z&key={key_id}&token={token_id}

        :param filter: Action types to filter, separated by comma or as a sequence.
        :type filter: ``str`` or ``list``

        :param since: Filter actions since specified date.
        :type since: ``str``

        :return: Events occurred in Trello list.
        :rtype: ``list`` of ``dict``
        """
        return self._client.fetch_json(
            '/lists/' + self._list.id + '/actions',
            query_params={
                'filter': filter,
                'since': since,
            })


def is_date(string):
    """
    Check if input string is date-formatted.

    :param string: Input date
    :type string: ``str``
    :rtype: ``bool``
    """
    try:
        dateutil.parser.parse(string)
        return True
    except ValueError:
        return False
