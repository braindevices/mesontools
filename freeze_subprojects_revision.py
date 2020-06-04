#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import os
from argparse import ArgumentParser
import wraptools

import logger_utils
logger, logger_both, stdout_handler = logger_utils.get_loggers(__name__)

def freeze_subprojects_revision(srcdir: str, dryrun: bool=True):
    subproject_names, wrap_files = wraptools.get_wrap_subprojects(srcdir)
    subdir_root = os.path.join(srcdir, 'subprojects')
    if not os.path.isdir(subdir_root):
        raise RuntimeError('{} is not a dir.'.format(subdir_root))
    for subproject in subproject_names:
        wraptools.change_subporject_revision_to_current_head(subdir_root, subproject, dryrun)


def parse_arguments():
    parser: ArgumentParser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="change all revision in wrap to current subproject's HEAD"
    )
    parser.add_argument(
        '--srcdir',
        dest='src_dir',
        required=True,
        help='source dir contains `subprojects/*.wrap`'
    )
    parser.add_argument(
        '--run',
        dest='dryrun',
        action='store_false',
        help='actually modify the wrap files.',
    )
    parser.add_argument(
        "-v", "--verbose",
        dest="verbose",
        action="count",
        help="set verbosity level [default: %(default)s]",
        default=0
    )
    return parser.parse_args()


def main():
    parsedargs = parse_arguments()
    logger_utils.config_loggers(parsedargs.verbose, [])
    freeze_subprojects_revision(parsedargs.src_dir, parsedargs.dryrun)

if __name__ == '__main__':
    main()