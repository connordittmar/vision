#!/usr/bin/env python
# make sure you set python path in terminal
# command: set PYTHONPATH = %PYTHONPATH%;
# Target Client
# This is the handler for posting images and targets.
# Both are manual inputs at this point

from __future__ import print_function
import argparse
import datetime
import getpass
import logging
import pprint
import sys
import time

from interop import AsyncClient
from interop import Target
from upload_targets import upload_targets

logger = logging.getLogger(__name__)

def targets(args,client):
    if args.legacy_filepath:
        if not args.target_dir:
            raise ValueError('--target_dir is required.')
        upload_legacy_targets(client, args.legacy_filepath, args.target_dir)
    elif args.target_dir:
        upload_targets(client, args.target_dir)
    else:
        targets = client.get_targets()
        for target in targets.result():
            pprint.pprint(target.serialize())

def main():
    #initialize logging
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')

    #parse command line args.
    parser = argparse.ArgumentParser(description='Async interop CLI.')
    parser.add_argument('--url',
                        required=True,
                        help='URL for server.')
    parser.add_argument('--username',
                        required=True,
                        help='Username for server login.')
    parser.add_argument('--password',help='Password for server login.')

    subparsers = parser.add_subparsers(help='Sub-command help.')

    subparser = subparsers.add_parser(
        'targets',
        help='Upload Targets.',
        description='''Download or upload targets to/from the interoperability
server.

Without extra arguments, this prints all targets that have been uploaded to the
server.

With --target_dir, this uploads new targets to the server.

This tool searches for target JSON and images files within --target_dir
conforming to the 2017 Object File Format and uploads the target
characteristics and thumbnails to the interoperability server.

Alternatively, if --legacy_filepath is specified, that file is parsed as the
legacy 2016 tab-delimited target file format. Image paths referenced in the
file are relative to --target_dir.

There is no deduplication logic. Targets will be uploaded multiple times, as
unique targets, if the tool is run multiple times.''',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparser.set_defaults(func=targets)
    subparser.add_argument(
         '--legacy_filepath',
         help='Target file in the legacy 2016 tab-delimited format.')
    subparser.add_argument(
         '--target_dir',
         help='Enables target upload. Directory containing target data.')

    # Parse args, get password
    args = parser.parse_args()
    if args.password:
        password = args.password
    else:
        password = getpass.getpass('Interoperability Password: ')

    # Create client and dispatch subcommand.
    client = AsyncClient(args.url, args.username, password)
    args.func(args, client)

if __name__ == '__main__':
    main()
