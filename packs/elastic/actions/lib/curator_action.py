from curator.api.utils import index_closed
from curator_api_commands import APICommands
from esbase_action import ESBaseAction
import logging
import sys

logger = logging.getLogger(__name__)


class CuratorAction(ESBaseAction):

    def __init__(self, config=None):
        super(CuratorAction, self).__init__(config=config)
        self.success = True
        self._act_on = None
        self._command = None
        self._api = None


    @property
    def act_on(self):
        if not self._act_on:
            _act_on = 'snapshots' if '.snapshots' in self.action else 'indices'
            self._act_on = _act_on
        return self._act_on

    @property
    def command(self):
        if not self._command:
            self._command = self.action.split('.')[0]
        return self._command

    @property
    def api(self):
        if not self._api:
            self._api = APICommands(**self.config)
        return self._api


    def show_dry_run(self):
        """
        Log dry run output with the command which would have been executed.
        """
        command = self.command
        items = self.api.fetch(act_on=self.act_on, nofilters_showall=True)
        print "DRY RUN MODE.  No changes will be made."
        for item in items:
            if self.act_on == 'snapshots':
                print "DRY RUN: {0}: {1}".format(command, item)
            else:
                print "DRY RUN: {0}: {1}{2}".format(command, item, ' (CLOSED)' if index_closed(self.client, item) else '')


    def do_show(self):
        """
        Show indices or snapshots command.
        """
        items = self.api.fetch(act_on=self.act_on, nofilters_showall=True)
        if not self.config.dry_run:
            for item in items:
                print item
        else:
            self.show_dry_run(items)
        sys.exit(0)


    def exit_msg(self, success):
        """
        Display a message corresponding to whether the job completed successfully or
        not, then exit.
        """
        if success:
            logger.info("Job completed successfully.")
        else:
            logger.warn("Job did not complete successfully.")
        sys.exit(0) if success else sys.exit(1)


    def do_command(self):
        """
        Do the command.
        """
        # Show and exit
        self.command == "show" and self.do_show()

        if self.config.dry_run:
            self.show_dry_run()
        else:
            logger.info("Job starting: {0} {1}".format(self.command, self.act_on))
            logger.debug("Params: {0}".format(self.config))

            success = self.api.invoke(command=self.action)
            self.exit_msg(success)
