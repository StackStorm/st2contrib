# pylint: disable=unexpected-keyword-arg
import dateutil.parser
from types import MethodType
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

        self._board_id = list_actions_sensor.get('board_id')
        if not self._board_id:
            raise ValueError('[TrelloListSensor]: "list_sensor.board_id" config value is required!')
        assert isinstance(self._board_id, basestring)

        self._list_id = list_actions_sensor.get('list_id')
        if not self._list_id:
            raise ValueError('[TrelloListSensor]: "list_sensor.list_id" config value is required!')
        assert isinstance(self._list_id, basestring)

        self._client = None

    @property
    def key_name(self):
        """
        Generate unique key name for built-in storage based on config values.

        :rtype: ``str``
        """
        return '{}.{}.date'.format(self._board_id, self._list_id)

    def setup(self):
        """
        Initiate connection to Trello API.
        """
        self._client = TrelloClient(api_key=self._config.get('api_key'),
                                   token=self._config.get('token') or None)

    def poll(self):
        """
        Fetch latest actions for Trello List, filter by type.
        Start reading feed where we stopped last time
        by passing `since` date parameter to Trello API.
        Save latest event `date` in st2 key-value storage.
        """
        _list = self._client.get_board(self._board_id).get_list(self._list_id)
        monkey_patch_trello(_list)
        _list.fetch_actions(
            action_filter=self._config['list_actions_sensor'].get('filter') or None,
            filter_since=self._sensor_service.get_value(self.key_name)
        )

        for action in reversed(_list.actions):
            self._sensor_service.dispatch(trigger=self.TRIGGER, payload=action)
            if is_date(action.get('date')):
                self._sensor_service.set_value(self.key_name, action.get('date'))

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


def monkey_patch_trello(trello_list):
    """
    Function to overwrite existing method in Trello List object.

    :param trello_list: Input Trello List object to monkey-patch.
    :type trello_list: :class:`trello.List`
    """
    def _fetch_actions(self, action_filter=None, filter_since=None):
        """
        Fetch actions for Trello List with possibility to specify filters.
        Example API request:
        https://api.trello.com/1/lists/{list_id}/actions?filter=createCard&since=2015-09-14T21:45:56.850Z&key={key_id}&token={token_id}

        :type self: :class:`trello.List`

        :param action_filter: Action types to filter, separated by comma or as a sequence.
        :type action_filter: ``str`` or ``list``

        :param filter_since: Filter actions since specified date.
        :type filter_since: ``str``

        :return: Events occurred in Trello list.
        :rtype: ``list`` of ``object``
        """
        json_obj = self.client.fetch_json(
            '/lists/' + self.id + '/actions',
            query_params={
                'filter': action_filter,
                'since': filter_since,
            })
        self.actions = json_obj
        return self.actions

    trello_list.fetch_actions = MethodType(_fetch_actions, trello_list)


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
