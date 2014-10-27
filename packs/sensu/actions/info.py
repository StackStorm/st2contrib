#!/usr/bin/python

from lib import sensu
import argparse

parser = argparse.ArgumentParser(description='Sensu System Info')

info = sensu.Status('config.yaml')

print(info.info())
