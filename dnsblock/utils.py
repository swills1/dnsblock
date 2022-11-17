# -*- coding: utf-8 -*-
import os
from pathlib import Path
from dnsblock import const


def get_source_path(env_var: str, default_path: str) -> str:
    final_path = Path(os.getenv(env_var, default_path)).expanduser().resolve()
    if not final_path.is_file():
        raise FileNotFoundError(f'File {final_path} does not exist')
    return final_path


def build_blocklist_list(source_path: str=None) -> list[str]:
    """Compile blocklists from source file into a Python list.

    :param source_path: Path to file containing blocklits to use
    :return: list of strings - urls
    """
    if source_path is not None:
        source_path = source_path
    else:
        source_path = get_source_path('DNSBLOCK_BLOCKLIST_PATH', const.DNSBLOCK_BLOCKLIST_PATH)
    with open(source_path) as f:
        source_path = f.read().splitlines()
    source_list = [u for u in source_path if not u.startswith('#')]
    return source_list
