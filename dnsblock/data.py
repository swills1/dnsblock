# -*- coding: utf-8 -*-
import requests
import concurrent.futures
import tomlkit
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from dnsblock import utils, const


@dataclass
class BlocklistResponse:
    url: str 
    success: bool
    text: Optional[str] = None


class BuildZone:
    def __init__(self, prefix, suffix, zone_path, url=None, source_zone_path=None):
        """Fetch all data from blocklist urls and trap specific errors.
        :param session: Requests session
        :param url: url of blocklist from source file
        :param timeout: number of seconds before Requests timeout
        :return: instance of BlocklistResponse
        """
        self.prefix = prefix
        self.suffix = suffix
        self.zone_path = zone_path
        self.url = url

    def fetch_blocklist_data(self, session: requests.Session, url: str, timeout: int) -> BlocklistResponse:
        """Fetch all data from blocklist urls and trap specific errors.
        :param session: Requests session
        :param url: url of blocklist from source file
        :param timeout: number of seconds before Requests timeout
        :return: instance of BlocklistResponse
        """
        try:
            with session.get(url, timeout=timeout) as response:
                return BlocklistResponse(url, True, response.text)
        except requests.exceptions.RequestException as e:
            return BlocklistResponse(url, False, '')

    def get_blocklist_data(self, timeout: int=10):
        """Use threading to process the source list and pull in fetched url data.
        :param timeout: Request timeout in seconds
        :return: results - all raw results returned from each blocklists
        :return: bad_urls - any url that does not have a 200 status code
        :return: good_urls - any url with a 200 status code
        """
        session = requests.Session()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            if self.url is not None:
                block_host = [self.url]
            else: block_host = utils.build_blocklist_list()
            for url in block_host:
                if not url.startswith('#'):
                    futures.append(executor.submit(self.fetch_blocklist_data, session, url, timeout))
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            bad_urls = [result.url for result in results if not result.success]
            good_urls = [result.url for result in results if result.success]
        return results, bad_urls, good_urls

    def unpack_blocklist_data(self) -> list[str]:
        """Turn get_blocklist_data results into list - includes IP if present
    
        :return: result_all - raw Requests results converted into a list
        """
        blocklist_data = self.get_blocklist_data()
        results = (blocklist_data[0])
        result = [obj.text for obj in results]
        for r in result:
            result_all = r.splitlines()
        return result_all

    def isolate_hostname(self) -> list[str]:
        """Isolate hostname when IP present and add just hostnames to list
        
        :return: :list: hostnames
        """
        blocklist_data = self.unpack_blocklist_data()
        hostnames = []
        for entry in blocklist_data:
            if not entry.startswith('#') and entry.strip() != '':
                hostname = entry.split()
                hostnames.append(hostname[-1])
        return hostnames

    def format_dnslist(self, prefix: str, suffix: str) -> list[str]:
        """Format DNS hostnames in preparation for zone conf file
    
        :param prefix: string before hostname for zone file formatting
        :param suffix: string behind hostname for zone file formatting
        :return: :list: zone_entry_list
        """
        hostnames = self.isolate_hostname()
        zone_entry_list = []
        for hostname in hostnames:
            zone_entry = prefix + hostname + suffix
            zone_entry_list.append(zone_entry)
        return zone_entry_list

    def build_zone_file(self):
        """Generate Recursive DNS zone file."""
        formatted_blocklist = self.format_dnslist(self.prefix, self.suffix)
        dateandtime = datetime.now()
        #date_string = dateandtime.strftime(config.GENERATED_DATETIME_FORMAT)
        with open(self.zone_path, 'w') as filehandle:
            generatedby_comment = dateandtime.strftime(const.GEN_COMMENT)
            filehandle.writelines(generatedby_comment)
            filehandle.writelines('server:\n')
            for url in formatted_blocklist:
                block_url = url + '\n'
                filehandle.writelines(block_url)

                
class CountHosts:
    def __init__(self, url=None):
        self.url = url

    def starts_with_hash(self, child: str) -> bool:
        """Exclude blocklist lines starting with #.

        :param child: UnicodeTranslateError
        :return: Boolean
        """
        if not child.startswith('#'):
            return True

    def fetch_blocklist_count(self, session: requests.Session, url: str, timeout: int) -> BlocklistResponse:
        """Perform entry count on blocklists
        
        :param session: requests.session
        :param url: Single url to get data from
        :param timeout: requests.session timeout in seconds
        """
        try:
            with session.get(url, timeout=timeout) as response:
                filterobj = filter(self.starts_with_hash, response.text.splitlines())
                red = len(list(filterobj))
                return url, red
        except requests.exceptions.RequestException as e:
            return 'booger'

    def get_count(self, url=None, timeout: int=10) -> requests.Response:
        """Count total entries per blocklist using threading.
        
        :param url: Single url to get data from
        :param timeout: requests.session timeout in seconds
        """
        session = requests.Session()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            if url:
                block_host = [url][0].split(', ')
            else: block_host = utils.build_blocklist_list()
            for blocklist in block_host:
                if not blocklist.startswith('#'):
                    futures.append(executor.submit(self.fetch_blocklist_count, session, blocklist, timeout))
            results = {future.result()[0]: future.result()[1] for future in concurrent.futures.as_completed(futures)}
            results.update({"Total": sum(results.values())})
        return results

    def show_count(self, url=None) -> str:
        """Show the count for every URL and perform a sum.
        By default, counts blocklist.txt.
        Takes url arg to count total entries for any given URL(s).
        
        :param url: (optional) List as string of urls to count.
        """
        if url:
            count_data = self.get_count(url)
        else: count_data = self.get_count()
        for key, value in count_data.items():
            print(f'{key} {value}')


def build_zone_file_toml():
    """Builds a zone file from values set in config file.
    Default config located at - ~/.config/dnsblock/config.toml
    Config location can be changed by usin env variable - DNSBLOCK_BLOCKLIST_PATH
    """
    toml_dict = tomlkit.loads(utils.get_source_path('DNSBLOCK_CONFIG_PATH', const.DNSBLOCK_CONFIG_PATH).read_text())
    if dd := toml_dict.get('default'):
        missing_keys = [key for key in ('zone_conf_path', 'prefix', 'suffix') if not dd.get(key)]
        if missing_keys:
            raise KeyError(f'Config file is missing key(s): {missing_keys}')
        else: 
            t = BuildConf(dd.get('prefix'), dd.get('suffix'), dd.get('zone_conf_path'))
            t.build_zone_file()
    else:
        raise KeyError('Config file missing the table "default"')
