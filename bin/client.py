#!/usr/bin/env python
# make sure you set python path in terminal
# command: set PYTHONPATH = %PYTHONPATH%;
# Target Client
# This is the handler for posting images and targets.
# Both are manual inputs at this point
# usage for import vision modules: from vision import ModuleName

# ! IMPORTANT: Run this in the vision master folder
# command line usage: python ./bin/client.py --url -----etc


from __future__ import print_function
import argparse
import datetime
import getpass
import logging
import pprint
import sys
import time

# This will only work if you have installed the interop module on your system
from interop import AsyncClient
from interop import Target
from upload_targets import upload_targets
from detect_duplicates import detect_duplicates
logger = logging.getLogger(__name__)

def targets(args,client):
    if args.target_dir:
        upload_targets(client, args.target_dir)
    else:
        targets = client.get_targets()
        for target in targets.result():
            pprint.pprint(target.id)

def remove_duplicates(args,client):
    targets = client.get_targets()
    pprint.pprint("Initial Target List:")
    for target in targets.result():
        pprint.pprint(target.id)
    duplicates = detect_duplicates(targets.result())
    pprint.pprint("Deleting Duplicates...")
    for duplicate in duplicates:
        pprint.pprint(duplicate)
        client.delete_target(duplicate)
    targets = client.get_targets()
    pprint.pprint("Remaining Targets:")
    for target in targets.result():
        pprint.pprint(target.id)
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
         '--target_dir',
         help='Enables target upload. Directory containing target data.')

    subparser = subparsers.add_parser(
        'remove_duplicates',
        help='Remove Duplicate Targets from server.',
        description='''.''',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparser.set_defaults(func=remove_duplicates)
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
