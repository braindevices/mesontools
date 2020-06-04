# -*- coding: UTF-8 -*-
import glob
from configparser import ConfigParser
import os

import typing
from io import StringIO

from mesonbuild.wrap import wrap

import git_helpers
import logger_utils
logger, logger_both, stdout_handler = logger_utils.get_loggers(__name__)

def parse_wrap(fpath: str):
    cgp = ConfigParser(interpolation=None)
    cgp.read(fpath)
    return cgp

# maybe we should import load_wrap from meson wraptool, instead of create our own parser?
def load_wrap(subdir_root: str, packagename: str):
    fpath = os.path.join(subdir_root, packagename + '.wrap')
    if os.path.isfile(fpath):
        return parse_wrap(fpath)
    return None


def get_rev_for_wrap_git(repo_dir: str, remote_url: str, remote_ref: str):
    rev = None
    if os.path.isdir(repo_dir):
        rev = git_helpers.get_revision_from_git_repo(repo_dir)
        if rev:
            return rev
    if remote_url and remote_ref:
        logger.info('cannot obtain revision from local git repo dir {}, try to obtain the remote one from {} ref={}.'.format(repo_dir, remote_url, remote_ref))
        rev = git_helpers.get_remote_hash_of_ref(remote_url, remote_ref)
    return rev


def get_current_subproject_revision(subdir_root: str, packagename: str):
    pkg, subproject_dir = wrap.get_directory(subdir_root, packagename)
    subproject_path = os.path.join(subdir_root, subproject_dir)
    if pkg.type == 'git':
        return get_rev_for_wrap_git(subproject_path, pkg.get('url'), pkg.get('revision'))
    else:
        logger.warning('does not support wrap type: {}'.format(pkg.type))



def save_wrap(subdir_root: str, packagename: str, wrap_config: ConfigParser, overwrite: bool):
    fpath = os.path.join(subdir_root, packagename + '.wrap')
    if os.path.exists(fpath):
        if overwrite and os.path.isfile(fpath):
            os.rename(fpath, fpath + '.orig')
        else:
            raise RuntimeError('wrap file {} exists.'.format(fpath))

    with open(fpath, 'w') as _f:
        wrap_config.write(_f)


def change_subporject_revision_to_current_head(subdir_root: str, packagename: str, dryrun: bool = True):
    pkg = wrap.load_wrap(subdir_root, packagename)
    wrap_config = pkg.config
    rev = get_current_subproject_revision(subdir_root, packagename)
    if rev:
        wrap_section = wrap_config.sections()[0]
        wrap_config[wrap_section]['revision'] = rev
        if dryrun:
            logger.warning('In dryrun mode, {}.wrap is not going to be modified.'.format(packagename))
            buffer = StringIO()
            wrap_config.write(buffer)
            print(buffer.getvalue())
            buffer.close()
        else:
            save_wrap(subdir_root, packagename, wrap_config, True)
    else:
        logger.info('cannot get revision for {}, keep its wrap file unmodified.'.format(packagename))


def get_wrap_subprojects(srcdir)->typing.Tuple[typing.List[str], typing.List[str]]:
    wraps = glob.glob(os.path.join(srcdir, 'subprojects', '*.wrap'))
    return [os.path.splitext(os.path.basename(_i))[0] for _i in wraps], wraps
