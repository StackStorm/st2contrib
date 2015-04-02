import argparse
import sys
import os
import subprocess
import select
import io


# Starts command in subprocess processing output as it appears.
def shell_out(command, env=None):
    env = env or {}
    env = os.environ.copy().update(env)
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
        self._keyname = {}
        for k, lg, kwargs in parser_options:
            self.parser.add_argument(k, lg, **kwargs)
            self._keyname[lg.lstrip('-')] = k

    def parse(self, argv=None):
        argv = argv or sys.argv[1:]
        return vars(self.parser.parse_args(args=argv))

    def short_arglist(self, kwargs=None):
        kwargs = kwargs or {}
        return self._arg_list(self.parse(), short=True)

    def long_arglist(self, kwargs=None):
        kwargs = kwargs or {}
        return self._arg_list(self.parse(), short=False)

    def _arg_list(self, kwargs, short=None):
        '''
        Returns list of command line arguments with short or long key names.
        '''
        cmd = []
        for n, v in (self.parse()).items():
            if not v:
                continue
            k = self._keyname[n] if short else n
            # We handle switch in case value is True
            cmd += [k] if v is True else [k, v]
        return cmd
