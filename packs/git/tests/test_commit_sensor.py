import os
import string
import random
import shutil

from st2tests.base import BaseSensorTestCase

from git_commit_sensor import GitCommitSensor

TEST_CONFIG = {
    'repositories': [
        {
            'url': 'https://github.com/StackStorm/st2',
            'branch': 'master',
            'local_clone_path': '/tmp/.test_st2_',
        },
        {
            'url': 'https://github.com/StackStorm/st2contrib.git',
            'branch': 'master',
            'local_clone_path': '/tmp/.test_st2contrib_',
        },
    ],
}


class GitCommitSensorTestCase(BaseSensorTestCase):
    sensor_cls = GitCommitSensor

    # A helper method to generate cloned directory name
    def _get_unique_path(self, basepath):
        path = basepath + random.choice(string.ascii_letters)
        if os.path.exists(path):
            path = self._get_unique_path(path)
        return path

    def tearDown(self):
        for repo in TEST_CONFIG['repositories']:
            shutil.rmtree(repo['local_clone_path'])

    def test_setup(self):
        # prepare the configuration params
        for repo in TEST_CONFIG['repositories']:
            repo['local_clone_path'] = self._get_unique_path(repo['local_clone_path'])

        sensor = self.get_sensor_instance(config=TEST_CONFIG)

        for repo in TEST_CONFIG['repositories']:
            self.assertFalse(os.path.exists(repo['local_clone_path']))

        # will clone repositories
        sensor.setup()

        for repo in TEST_CONFIG['repositories']:
            self.assertTrue(os.path.exists(os.path.join(repo['local_clone_path'], '.git')))

        sensor.poll()

        self.assertEqual(len(self.get_dispatched_triggers()), 2)
        self.assertTriggerDispatched(trigger='git.head_sha_monitor')

        # clear informations of past dispatching
        self.sensor_service.dispatched_triggers = []

        sensor.poll()

        self.assertEqual(len(self.get_dispatched_triggers()), 0)
