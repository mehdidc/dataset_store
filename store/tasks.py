import os
import urllib
from collections import namedtuple

from invoke import task

import helpers
import config


Host = namedtuple('Host', ['name', 'addr', 'port'])
stores_folder = os.path.join(os.getenv("HOME"), ".stores")
list_filename = "list"


@task
def add_myself():

    myself = get_myself_()

    repo = get_or_clone_stores_repo_(stores_folder)

    list_filename_abs = os.path.join(stores_folder, list_filename)
    myself_content = build_content_(myself)
    if myself_content in open(list_filename_abs).readlines():
        return
    with open(list_filename_abs, "a") as fd:
        fd.write(myself_content)
    repo.index.add([list_filename])
    repo.index.commit("update stores")
    repo.remotes.origin.push()


@task
def clean_store_list():
    repo = get_or_clone_stores_repo_(stores_folder)  # NOQA
    list_filename_abs = os.path.join(stores_folder, list_filename)
    with open(list_filename_abs, "r") as fd:
        lines = list(fd.readlines())

    stores = map(get_from_content_, lines)
    stores = filter(host_is_alive_, stores)
    new_lines = map(build_content_, stores)

    with open(list_filename_abs, "w") as fd:
        for line in new_lines:
            fd.write(line + "\n")
    repo.index.add([list_filename])
    repo.index.commit("clean stores")
    repo.remotes.origin.push()


def get_mirror():
    import random
    mirrors = get_mirrors()
    return random.choice(mirrors)


def get_mirrors():
    repo = get_or_clone_stores_repo_(stores_folder)  # NOQA
    list_filename_abs = os.path.join(stores_folder, list_filename)
    with open(list_filename_abs) as fd:
        mirrors = map(get_from_content_, fd.readlines())
    return mirrors


def build_content_(host):
    return "{} {}".format(host.name, host.addr)


def get_from_content_(s):
    name, addr = s.split(" ")
    return Host(name=name, addr=addr)


def get_or_clone_stores_repo_(folder):
    from git import Repo
    git_repo = config.store_list_repo
    if os.path.exists(folder):
        repo = Repo(folder)
    else:
        repo = Repo.clone_from(git_repo,
                               folder,
                               branch='master')
    return repo


def host_is_alive_(host):
    return is_alive_("http://{}:{}".format(host.addr, host.port))


def is_alive_(url):
    try:
        return urllib.urlopen(url).getcode() == 200
    except IOError:
        return False


def get_myself_():
    return Host(name=helpers.get_host_name(),
                addr=helpers.get_host_ip(),
                port=config.port)
