from collections import defaultdict
import argparse
import sys
import os
import subprocess
import select
import io


# Starts command in subprocess processing output as it appears.
def shell_out(command, env=None):
    env = os.environ.copy().update(env or {})
    shell = False if isinstance(command, list) else True
    proc = subprocess.Popen(args=command, stdin=None, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, env=env, shell=shell)
    while True:
        fdlist = [proc.stdout.fileno(), proc.stderr.fileno()]
        ios = select.select(fdlist, [], [])
        for fd in ios[0]:
            if fd == proc.stdout.fileno():
                sys.stdout.write(proc.stdout.read(io.DEFAULT_BUFFER_SIZE))
            else:
                sys.stderr.write(proc.stderr.read(io.DEFAULT_BUFFER_SIZE))

        if proc.poll() is not None:
            break
    return proc.returncode


class CmdlineParser(object):
    def __init__(self, parser_options):
        '''
        Initialize argument parser with argument triplets as the following:
            [
                ('-j', '--attributes', {}),
                ...
                ('-W', '--why_run', {'action': 'store_true'}),
            ]
        '''
        self.parser = argparse.ArgumentParser()
        self._name_to_key = defaultdict(lambda: None)

        for k, lk, kwargs in parser_options:
            long_name = lk.lstrip('-')
            # Short keys might be missing, so filter None's
            keys = (i for i in (k, lk) if i is not None)
            self.parser.add_argument(*(keys), **kwargs)
            self.name_to_key[long_name] = k

    @property
    def raw_parser(self):
        return self.parser

    @property
    def name_to_key(self):
        return self._name_to_key

    def parse(self, argv=None):
        argv = argv or sys.argv[1:]
        return vars(self.parser.parse_args(args=argv))

    def short_arglist(self, kwargs=None):
        kwargs = kwargs or self.parse()
        return self._arg_list(kwargs, short=True)

    def long_arglist(self, kwargs=None):
        kwargs = kwargs or self.parse()
        return self._arg_list(kwargs, short=False)

    def _arg_list(self, kwargs, short=None):
        '''Returns list of command line arguments with short or long key names.
        Function recieves dict with long key names always, because action runner
        support only long names.
        '''
        cmd = []
        having_value = ((k, v) for k, v in kwargs.items() if v is not None)

        for long_name, value in having_value:
            do_short = short
            # Short key might not exist, we should use long name.
            if self.name_to_key[long_name] is None:
                do_short = False

            if do_short:
                key = self.name_to_key[long_name]
            else:
                key = "--{}".format(long_name)

            # Handle switch in case value when True/False
            if value is True:
                cmd += [key]
            elif value is False:
                pass
            else:
                cmd += [key, value]

        return cmd
