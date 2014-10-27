#!/usr/bin/python

from lib import sensu
import argparse
import sys

parser = argparse.ArgumentParser(description='Sensu System Info')

info = sensu.Status('config.json')

print info.info()
