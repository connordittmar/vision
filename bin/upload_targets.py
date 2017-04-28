# Module to load targets from file and upload via interoperability.

import csv
import imghdr
import json
import logging
import os
import pprint
import re

from interop import Target

logger = logging.getLogger(__name__)

TARGET_TYPE_MAP = {'STD': 'standard', 'OAX': 'off_axis', 'EMG': 'emergent', }

LATITUDE_REGEX = re.compile(
    '(?P<dir>[NS])(?P<deg>\d\d) (?P<min>\d\d) (?P<sec>\d\d\.\d{0,3})')
LATITUDE_DIR = {'S': -1, 'N': 1}
LONGITUDE_REGEX = re.compile(
    '(?P<dir>[EW])(?P<deg>\d\d\d) (?P<min>\d\d) (?P<sec>\d\d\.\d{0,3})')
LONGITUDE_DIR = {'E': -1, 'W': 1}


def upload_target(client,
                  target_file,
                  image_file,
                  team_id=None,
                  actionable_override=None):
    """Upload a single target to the server

    Args:
        client: interop.Client connected to the server
        target_file: Path to file containing target details in the Object
            File Format.
        image_file: Path to target thumbnail. May be None.
        team_id: The username of the team on whose behalf to submit targets.
            Defaults to None.
        actionable_override: Manually sets the target to be actionable. Defaults
            to None.
    """
    with open(target_file) as f:
        target = Target.deserialize(json.load(f))
        id = target.id
    target.team_id = team_id
    target.actionable_override = actionable_override
    logger.info('Uploading target %s: %r' % (target_file, target))
    target = client.post_target(target)
    if image_file:
        logger.info('Uploading target thumbnail %s' % image_file)
        with open(image_file) as img:
            client.post_target_image(id, img.read())
    else:
        logger.warning('No thumbnail for target %s' % target_file)


def upload_targets(client, target_dir, team_id=None, actionable_override=None):
    """Upload all targets found in directory

    Args:
        client: interop.Client connected to the server
        target_dir: Path to directory containing target files in the Object
            File Format and target thumbnails.
        team_id: The username of the team on whose behalf to submit targets.
            Defaults to None.
        actionable_override: Optional. Overrides the target as actionable. Must
            be superuser to set.
    """
    targets = {}
    images = {}

    for entry in os.listdir(target_dir):
        name, ext = os.path.splitext(entry)

        if ext.lower() == '.json':
            if name in targets:
                raise ValueError(
                    'Found duplicate target files for %s: %s and %s' %
                    (name, targets[name], entry))
            targets[name] = os.path.join(target_dir, entry)
        elif ext.lower() in ['.png', '.jpg', '.jpeg']:
            if name in images:
                raise ValueError(
                    'Found duplicate target images for %s: %s and %s' %
                    (name, images[name], entry))
            images[name] = os.path.join(target_dir, entry)

    pairs = {}
    for k, v in targets.items():
        if k in images:
            pairs[v] = images[k]
        else:
            pairs[v] = None

    logger.info('Found target-image pairs:\n%s' % pprint.pformat(pairs))

    for target, image in pairs.items():
        upload_target(client, target, image, team_id, actionable_override)
