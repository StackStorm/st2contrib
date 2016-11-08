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
        self._git_repositories = []
        self._trigger_name = 'head_sha_monitor'
        self._trigger_pack = 'git'
        self._trigger_ref = '.'.join([self._trigger_pack, self._trigger_name])

    def setup(self):
        git_opts = self._config

        # update internal variable which specifies interval to dispatch poll
        interval = git_opts.get('poll_interval', None)
        if interval is not None:
            self.set_poll_interval(interval)

        for opts in git_opts['repositories']:
            try:
                repo_local, repo_remote = self._prepare_local_repository(opts)
                self._git_repositories.append({
                    'local': repo_local,
                    'remote': repo_remote,
                    'old_head': None,
                })
            except Exception as e:
                # Whan an exception is occurred during preparation,
                # this only output error message and ignores it to poll events.
                self._logger.exception(str(e))

    def poll(self):
        for repo in self._git_repositories:
            # Fetch new commits
            try:
                pulled = repo['remote'].pull()
                if pulled:
                    self._logger.debug('Pulled info from remote repo. %s', pulled[0].commit)
                else:
                    self._logger.debug('Nothing pulled from remote repo.')
            except:
                self._logger.exception('Failed git pull from remote repo.')

            head = repo['local'].commit()
            head_sha = head.hexsha

            if not repo['old_head']:
                repo['old_head'] = head_sha

                # There is exactly one commit. Kick off a trigger.
                if len(repo['local'].heads) == 1:
                    self._dispatch_trigger(head, repo['local'])
            elif head_sha != repo['old_head']:
                try:
                    self._dispatch_trigger(head, repo['local'])
                except Exception:
                    self._logger.exception('Failed dispatching trigger.')
                else:
                    repo['old_head'] = head_sha

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _dispatch_trigger(self, commit, repo):
        trigger = self._trigger_ref
        payload = {}
        payload['branch'] = repo.active_branch.name
        payload['revision'] = str(commit)
        payload['author'] = commit.author.name
        payload['author_email'] = commit.author.email
        payload['authored_date'] = self._to_date(commit.authored_date)
        payload['author_tz_offset'] = commit.author_tz_offset
        payload['committer'] = commit.committer.name
        payload['committer_email'] = commit.committer.email
        payload['committed_date'] = self._to_date(commit.committed_date)
        payload['committer_tz_offset'] = commit.committer_tz_offset
        payload['repository_url'] = repo.config_reader().get_value('remote "origin"', 'url')
        self._logger.debug('Found new commit. Dispatching trigger: %s', payload)
        self._sensor_service.dispatch(trigger, payload)

    def _to_date(self, ts_epoch):
        return datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%dT%H:%M:%SZ')

    def _prepare_local_repository(self, opts):
        url = opts['url']
        branch = opts['branch']

        if url is None:
            raise Exception('Remote git URL not set.')

        # set local repository path to be cloned
        repo_name = url[url.rindex('/') + 1:]
        default_clone_dir = os.path.join(os.path.dirname(__file__), 'clones', repo_name)
        local_path = opts.get('local_clone_path', default_clone_dir)

        # create a directory to store cloned repositories
        if not os.path.exists(os.path.dirname(local_path)):
            os.mkdir(os.path.dirname(local_path), 0755)

        if os.path.exists(local_path):
            repo_local = Repo.init(local_path)
        else:
            try:
                repo_local = Repo.clone_from(url, local_path, branch=branch)
            except Exception as e:
                raise Exception('Unable to clone remote repo from %s [%s]: %s' %
                                (url, branch, str(e)))

        return repo_local, repo_local.remote('origin')
