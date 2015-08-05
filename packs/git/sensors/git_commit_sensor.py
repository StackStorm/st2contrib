#!/usr/bin/env python

# Requirements
# pip install gitpython
# Also requires git CLI tool to be installed.

import os
import datetime

from git.repo import Repo

from st2reactor.sensor.base import PollingSensor


class GitCommitSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(GitCommitSensor, self).__init__(sensor_service=sensor_service,
                                              config=config,
                                              poll_interval=poll_interval)

        self._logger = self._sensor_service.get_logger(__name__)
        self._old_head = None
        self._remote = None
        self._trigger_name = 'head_sha_monitor'
        self._trigger_pack = 'git'
        self._trigger_ref = '.'.join([self._trigger_pack, self._trigger_name])

    def setup(self):
        git_opts = self._config

        if git_opts['url'] is None:
            raise Exception('Remote git URL not set.')

        self._url = git_opts['url']
        default_clone_dir = os.path.join(os.path.dirname(__file__), 'clones')
        self._local_path = git_opts.get('local_clone_path', default_clone_dir)
        self._poll_interval = git_opts.get('poll_interval', self._poll_interval)

        if os.path.exists(self._local_path):
            self._repo = Repo.init(self._local_path)
        else:
            try:
                self._repo = Repo.clone_from(self._url, self._local_path)
            except Exception:
                self._logger.exception('Unable to clone remote repo from %s',
                                       self._url)
                raise

        self._remote = self._repo.remote('origin')

    def poll(self):
        # Fetch new commits
        try:
            pulled = self._remote.pull()
            if pulled:
                self._logger.debug('Pulled info from remote repo. %s', pulled[0].commit)
            else:
                self._logger.debug('Nothing pulled from remote repo.')
        except:
            self._logger.exception('Failed git pull from remote repo.')

        head = self._repo.commit()
        head_sha = head.hexsha

        if not self._old_head:
            self._old_head = head_sha
            if len(self._repo.heads) == 1:  # There is exactly one commit. Kick off a trigger.
                self._dispatch_trigger(head)
            return

        if head_sha != self._old_head:
            try:
                self._dispatch_trigger(head)
            except Exception:
                self._logger.exception('Failed dispatching trigger.')
            else:
                self._old_head = head_sha

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _dispatch_trigger(self, commit):
        trigger = self._trigger_ref
        payload = {}
        payload['branch'] = self._repo.active_branch.name
        payload['revision'] = str(commit)
        payload['author'] = commit.author.name
        payload['author_email'] = commit.author.email
        payload['authored_date'] = self._to_date(commit.authored_date)
        payload['author_tz_offset'] = commit.author_tz_offset
        payload['committer'] = commit.committer.name
        payload['committer_email'] = commit.committer.email
        payload['committed_date'] = self._to_date(commit.committed_date)
        payload['committer_tz_offset'] = commit.committer_tz_offset
        self._logger.debug('Found new commit. Dispatching trigger: %s', payload)
        self._sensor_service.dispatch(trigger, payload)

    def _to_date(self, ts_epoch):
        return datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%dT%H:%M:%SZ')
