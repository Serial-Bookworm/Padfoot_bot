import re
import requests
import json
import time

from botutils.constants import AO3_CHECK_STR, HS_API_URL_AO3
from botutils.embeds import get_embeds_ao3

class Ao3Searcher:
    def __init__(self, message):
        self.message = message
        self.all_links_to_get_stories_for = []
        self.res_metadata = None
        self.res_embeds = None



    def execute_search(self):
        """the main function to execute ao3 search/scrape
        """
        self.find_links_in_message()
        
        self.get_metadata()
        
        self.fetch_ao3_embeds()

        return self.res_embeds

    

    def find_links_in_message(self):
        """find all ao3 links in message
        """
        all_links = re.findall(r'(https?://[^\s]+)', self.message)
        all_links_to_get_stories_for = []
        for link in all_links:
            if AO3_CHECK_STR in link:
                all_links_to_get_stories_for.append(link)
        self.all_links_to_get_stories_for = all_links_to_get_stories_for



    def get_metadata(self):
        """Return a list of metadata for a list of links passed

        Args:
            all_links_to_get_stories_for ([list]): list of ao3 links 

        Returns:
            [list]: list of metadata
        """
        res_metadata = []
        for link in self.all_links_to_get_stories_for:
            try:
                story_id = link[link.index('works/')+len('works/') : link.index('/', link.index('works/')+6)]
            except:
                story_id = link[link.index('works/')+len('works/') :]
            try:    
                response = requests.get(f'{HS_API_URL_AO3}/{story_id}')
                data = json.loads(response.text)
                res_metadata.append(data)
                time.sleep(2)
            except:
                print('Could not get metadata response for: ', story_id)
                time.sleep(2)
        
        self.res_metadata = res_metadata



    def fetch_ao3_embeds(self):
        """gets embeds for all links for ao3
        """
        self.res_embeds = get_embeds_ao3(self.res_metadata)

    