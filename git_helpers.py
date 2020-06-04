# -*- coding: UTF-8 -*-
import git
import logging
import gitdb
import logger_utils
logger, logger_both, stdout_handler = logger_utils.get_loggers(__name__)
import traceback
import os

def get_remote_hash_of_ref(url: str, ref: str):
    git_cmd = git.cmd.Git()
    try:
        out = git_cmd.ls_remote(url, ref)
        if out:
            return out.split('\t')[0]
    except git.GitCommandError as e:
        logger.warning(e)
    return None


def get_revision_from_git_repo(repopath: str, ref='HEAD'):
    rev = None
    try:
        repo = git.Repo(repopath)
        rev = repo.rev_parse(ref).hexsha
    except (git.InvalidGitRepositoryError, gitdb.exc.BadName, gitdb.exc.BadObject) as e:
        msg = '\n\t'.join(traceback.format_exc().strip().split(os.linesep))
        logger.warning(msg)
    return rev