import os
import requests
from dnsblock import const

def get_source_path():
    """Get the path to the source file containing blocklists to use.

    By default the path is ~/dnsblock/blocklists.txt.
    The default path can be changed using env variable DNSBLOCK_SOURCE_PATH.
    """
    default_path = os.path.expanduser(const.DNSBLOCK_SOURCE_PATH)
    final_path = os.environ.get('DNSBLOCK_SOURCE_PATH', default_path)
    return final_path


def build_source_list(source_path: str=None) -> list[str]:
    """Compile blocklists from source file into a Python list.

    :param source_path: Path to file containing blocklits to use
    :return: list of strings - urls
    """
    if source_path is not None:
        source_path = source_path
    else:
        source_path = get_source_path()
    with open(source_path) as f:
        source_path = f.read().splitlines()
    source_list = [u for u in source_path if not u.startswith('#')]
    return source_list


def fetch_single_blocklist(url: str=None) -> list[str]:
    """Get DNS entries from a single blocklist by specifying the url.
    
    :param url: Url of blocklist containing DNS entries
    :return: List of strings - dns hostname entries
    """
    if url:
        response = requests.get(url)
        blocklist_data = []
        if response.status_code == 200:
            response_text_list = response.text.splitlines()
            for line in response_text_list:
                if line and not line.startswith('#'):
                    domain_name = line.split(' ')[-1]
                    if domain_name != 'localhost':
                        blocklist_data.append(domain_name)
    else:
        return 'No url'
    return  blocklist_data
