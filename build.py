#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from cpt.packager import ConanMultiPackager
from socket import gethostbyname_ex
from urllib.parse import urlparse
from dotenv import load_dotenv


def __host_mappings():
    # used to mitigate docker limitations when accessing private dns over vpn
    # https://github.com/docker/for-mac/issues/2820
    remotes = os.getenv("CONAN_REMOTES", None)
    if not remotes:
        return None

    urls = remotes.split(',')

    mappings = list()
    for url in urls:
        hostname = urlparse(url).hostname
        address = gethostbyname_ex(hostname)[-1]
        mappings.append(f"--add-host={hostname}:{address[0]}")

    return " ".join(mappings)


if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    builder = ConanMultiPackager(
        build_policy='missing',
        use_docker=True,
        docker_run_options=__host_mappings())
    builder.add_common_builds()
    builder.run()
