import re
import requests
import json
import time

from botutils.constants import PORTKEY_CHECK_STR, PORTKEY_API_STORY
from botutils.embeds import get_embeds_portkey

class PortkeySearcher:
    def __init__(self, message):
        self.message = message
        self.all_links_to_get_stories_for = []
        self.res_metadata = None
        self.res_embeds = None

    def execute_search(self):
        """main function to execute portkey search/scrape
        """
        self.find_links_in_message()

        self.get_metadata()
        
        self.fetch_portkey_embeds() 
        
        return self.res_embeds


    def find_links_in_message(self):
        """find all portkey links in message
        """
        all_links = re.findall(r'(https?://[^\s]+)', self.message)
        all_links_to_get_stories_for = []
        for link in all_links:
            if PORTKEY_CHECK_STR in link:
                all_links_to_get_stories_for.append(link)
        self.all_links_to_get_stories_for = all_links_to_get_stories_for


    def get_metadata(self):
        """Return a list of metadata for a list of links passed

        Args:
            all_links_to_get_stories_for ([list]): list of portkey links 

        Returns:
            [list]: list of metadata
        """
        res_metadata = []
        
        for link in self.all_links_to_get_stories_for:
            try:
                story_id = link[link.index('story/')+6 : link.index('/', link.index('story/')+6)].strip()
            except:
                story_id = link[link.index('story/')+6 :].strip()
            try:
                response = requests.get(f'{PORTKEY_API_STORY}{story_id}/meta')
                data = json.loads(response.text)
                res_metadata.append(data)
                time.sleep(2)
            except:
                print('Could not get metadata response for: ', story_id)
                time.sleep(2)
        
        self.res_metadata = res_metadata


    def fetch_portkey_embeds(self):
        self.res_embeds = get_embeds_portkey(self.res_metadata)



    