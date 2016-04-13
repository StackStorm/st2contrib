from st2tests.base import BaseActionTestCase

from lib.mssql_action import MSSQLAction


class MSSQLExampleAction(MSSQLAction):
    def run(self):
        pass


# noinspection PyProtectedMemberInspection
class MSSQLActionTestCase(BaseActionTestCase):
    action_cls = MSSQLExampleAction

    def test_connect_none(self):
        action = self.get_action_instance()
        action.config = {}
        self.assertRaises(Exception, action._connect_params)

    def test_connect_config(self):
        action = self.get_action_instance()
        action.config = {
            'default': 'db2',
            'db1': {
                'server': 'ahost1',
                'user': 'auser',
                'password': 'apass'
            },
            'db2': {
                'server': 'bhost1',
                'user': 'buser',
                'password': 'bpass'
            }
        }
        expected = {'database': 'db2', 'server': 'bhost1', 'user': 'buser', 'password': 'bpass'}
        self.assertEqual(expected, action._connect_params())

    def test_connect_config_database(self):
        action = self.get_action_instance()
        action.config = {
            'default': 'db2',
            'db1': {
                'server': 'ahost1',
                'user': 'auser',
                'password': 'apass'
            },
            'db2': {
                'database': 'wtdb',
                'server': 'bhost1',
                'user': 'buser',
                'password': 'bpass'
            }
        }
        expected = {'database': 'wtdb', 'server': 'bhost1', 'user': 'buser', 'password': 'bpass'}
        self.assertEqual(expected, action._connect_params())

    def test_connect_manual(self):
        action = self.get_action_instance()
        action.config = {}
        expected = {'database': 'db3', 'server': 'mhost1', 'user': 'muser', 'password': 'mpass'}
        self.assertEqual(expected, action._connect_params(
            database='db3',
            server='mhost1',
            user='muser',
            password='mpass'
        ))

    def test_connect_manual_database(self):
        action = self.get_action_instance()
        action.config = {
            'db1': {
                'server': 'ahost1',
                'user': 'auser',
                'password': 'apass'
            },
            'db2': {
                'server': 'bhost1',
                'user': 'buser',
                'password': 'bpass'
            }
        }
        expected = {'database': 'db1', 'server': 'ahost1', 'user': 'auser', 'password': 'apass'}
        self.assertEqual(expected, action._connect_params(database='db1'))

    def test_connect_override(self):
        action = self.get_action_instance()
        action.config = {
            'default': 'db2',
            'db1': {
                'server': 'ahost1',
                'user': 'auser',
                'password': 'apass'
            },
            'db2': {
                'server': 'bhost1',
                'user': 'buser',
                'password': 'bpass'
            }
        }
        expected = {'database': 'db1', 'server': 'mhost1', 'user': 'muser', 'password': 'apass'}
        self.assertEqual(expected, action._connect_params(
            database='db1',
            server='mhost1',
            user='muser',
        ))

    def test_connect_unlisted_database(self):
        action = self.get_action_instance()
        action.config = {
            'default': 'unknown-db',
            'db1': {
                'server': 'ahost1'
            }
        }
        self.assertRaises(Exception, action._connect_params)

    def test_connect_missing_database(self):
        action = self.get_action_instance()
        action.config = {
            'db1': {
                'server': 'ahost1',
                'user': 'auser',
                'password': 'apass'
            }
        }
        self.assertRaises(Exception, action._connect_params)

    def test_connect_missing_server(self):
        action = self.get_action_instance()
        action.config = {
            'default': 'db1',
            'db1': {
                'user': 'auser',
                'password': 'apass'
            }
        }
        self.assertRaises(Exception, action._connect_params)

    def test_connect_missing_user(self):
        action = self.get_action_instance()
        action.config = {
            'default': 'db1',
            'db1': {
                'server': 'ahost1',
                'password': 'apass'
            }
        }
        self.assertRaises(Exception, action._connect_params)

    def test_connect_missing_password(self):
        action = self.get_action_instance()
        action.config = {
            'default': 'db1',
            'db1': {
                'server': 'ahost1',
                'user': 'auser'
            }
        }
        self.assertRaises(Exception, action._connect_params)
