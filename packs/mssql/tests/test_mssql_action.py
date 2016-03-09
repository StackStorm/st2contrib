from st2tests.base import BaseActionTestCase

from lib.mssql_action import MSSQLAction


# noinspection PyProtectedMemberInspection
class MSSQLActionTestCase(BaseActionTestCase):
    action_cls = MSSQLAction

    def test_connect_none(self):
        action = self.get_action_instance()
        setattr(action, 'config', {})
        self.assertRaises(Exception, action._connect_params)

    def test_connect_config(self):
        action = self.get_action_instance()
        setattr(action, 'config', {
            'database': 'another-db',
            'some-db': {
                'server': 'aserver1',
                'user': 'auser',
                'password': 'apass'
            },
            'another-db': {
                'server': 'bserver1',
                'user': 'buser',
                'password': 'bpass'
            }
        })
        expected = {'database': 'another-db', 'server': 'bserver1', 'user': 'buser', 'password': 'bpass'}
        self.assertEqual(expected, action._connect_params())

    def test_connect_config_database(self):
        action = self.get_action_instance()
        setattr(action, 'config', {
            'database': 'another-db',
            'some-db': {
                'server': 'aserver1',
                'user': 'auser',
                'password': 'apass'
            },
            'another-db': {
                'database': 'another-name',
                'server': 'bserver1',
                'user': 'buser',
                'password': 'bpass'
            }
        })
        expected = {'database': 'another-name', 'server': 'bserver1', 'user': 'buser', 'password': 'bpass'}
        self.assertEqual(expected, action._connect_params())

    def test_connect_manual(self):
        action = self.get_action_instance()
        setattr(action, 'config', {})
        expected = {'database': 'manual-db', 'server': 'mserver1', 'user': 'muser', 'password': 'mpass'}
        self.assertEqual(expected, action._connect_params(
            database='manual-db',
            server='mserver1',
            user='muser',
            password='mpass'
        ))

    def test_connect_manual_database(self):
        action = self.get_action_instance()
        setattr(action, 'config', {
            'some-db': {
                'server': 'aserver1',
                'user': 'auser',
                'password': 'apass'
            },
            'another-db': {
                'server': 'bserver1',
                'user': 'buser',
                'password': 'bpass'
            }
        })
        expected = {'database': 'some-db', 'server': 'aserver1', 'user': 'auser', 'password': 'apass'}
        self.assertEqual(expected, action._connect_params(database='some-db'))

    def test_connect_override(self):
        action = self.get_action_instance()
        setattr(action, 'config', {
            'database': 'another-db',
            'some-db': {
                'server': 'aserver1',
                'user': 'auser',
                'password': 'apass'
            },
            'another-db': {
                'server': 'bserver1',
                'user': 'buser',
                'password': 'bpass'
            }
        })
        expected = {'database': 'some-db', 'server': 'mserver1', 'user': 'muser', 'password': 'bpass'}
        self.assertEqual(expected, action._connect_params(
            database='some-db',
            server='mserver1',
            user='muser',
        ))

    def test_connect_unlisted_database(self):
        action = self.get_action_instance()
        setattr(action, 'config', {
            'database': 'unknown-db',
            'some-db': {
                'server': 'aserver1'
            }
        })
        self.assertRaises(Exception, action._connect_params)

    def test_connect_missing_database(self):
        action = self.get_action_instance()
        setattr(action, 'config', {
            'some-db': {
                'server': 'aserver1',
                'user': 'auser',
                'password': 'apass'
            }
        })
        self.assertRaises(Exception, action._connect_params)

    def test_connect_missing_server(self):
        action = self.get_action_instance()
        setattr(action, 'config', {
            'database': 'some-db',
            'some-db': {
                'user': 'auser',
                'password': 'apass'
            }
        })
        self.assertRaises(Exception, action._connect_params)

    def test_connect_missing_user(self):
        action = self.get_action_instance()
        setattr(action, 'config', {
            'database': 'some-db',
            'some-db': {
                'server': 'aserver1',
                'password': 'apass'
            }
        })
        self.assertRaises(Exception, action._connect_params)

    def test_connect_missing_password(self):
        action = self.get_action_instance()
        setattr(action, 'config', {
            'database': 'some-db',
            'some-db': {
                'server': 'aserver1',
                'user': 'auser'
            }
        })
        self.assertRaises(Exception, action._connect_params)
