import re
import requests
import json
import time

from botutils.constants import FFN_CHECK_STR, HS_API_URL_FFN
from botutils.embeds import get_embeds_ffn

class FFnSearcher:
    def __init__(self, message):
        self.message = message
        self.all_links_to_get_stories_for = []
        self.res_metadata = None
        self.res_embeds = None

    def execute_search(self):
        """main function to execute ffn search/scrape
        """
        self.find_links_in_message()

        self.get_metadata()
        
        self.fetch_ffn_embeds() 
        
        return self.res_embeds


    def find_links_in_message(self):
        """find all ffn links in message
        """
        all_links = re.findall(r'(https?://[^\s]+)', self.message)
        all_links_to_get_stories_for = []
        for link in all_links:
            if FFN_CHECK_STR in link:
                all_links_to_get_stories_for.append(link)
        self.all_links_to_get_stories_for = all_links_to_get_stories_for


    def get_metadata(self):
        """Return a list of metadata for a list of links passed

        Args:
            all_links_to_get_stories_for ([list]): list of ffnet links 

        Returns:
            [list]: list of metadata
        """
        res_metadata = []
        
        for link in self.all_links_to_get_stories_for:
            try:
                story_id = link[link.index('s/')+2 : link.index('/', link.index('s/')+4)]
            except:
                story_id = link[link.index('s/')+2 :]
            try:
                response = requests.get(f'{HS_API_URL_FFN}/{story_id}')
                data = json.loads(response.text)
                res_metadata.append(data)
                time.sleep(2)
            except Exception as e:
                print(e)
                print('Could not get metadata response for: ', story_id)
                time.sleep(2)
        
        self.res_metadata = res_metadata


    def fetch_ffn_embeds(self):
        self.res_embeds = get_embeds_ffn(self.res_metadata)



    