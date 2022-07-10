import re
from botutils.constants import AO3_AUTHOR_CHECK_STR, HS_API_AU_AO3_URL
from bs4 import BeautifulSoup
import requests
import json

class AO3AuProfiler:
    def __init__(self, msg) -> None:
        self.message = msg
        self.au_link = None
        self.au_name = None
        self.au_intro_line = None
        self.au_story_details = None

        # start the au profile crawl
        self._execute_au_crawl()

    def _execute_au_crawl(self):
        self._fetch_au_link_from_message()
        self._crawl_au_profile_ao3()

    def _fetch_au_link_from_message(self):
        """extract author profile ao3 link from message text"""

        try:
            all_links = re.findall(r'(https?://[^\s]+)', self.message)
            all_links_to_get_profiles_for = []
            for link in all_links:
                if AO3_AUTHOR_CHECK_STR in link:
                    all_links_to_get_profiles_for.append(link)
                    break # get only the first profile link
            
            self.au_link = all_links_to_get_profiles_for[0]
        except:
            print("No ao3 au link found.")

    def _crawl_au_profile_ao3(self):
        """to crawl au profile link fetched"""
        
        link = self.au_link
        try:
            au_id = link[link.index('users/')+6 : link.rindex('/works')]
        except:
            au_id = link[link.index('users/')+6 : ]
        if not au_id:
            try:
                au_id = link[link.index('users/')+6 : link.rindex('/pseuds')]
            except:
                au_id = link[link.index('users/')+6 : ]
        
        if "/" in au_id:
            au_id = au_id[:au_id.index("/")]
        print(au_id)
        response = requests.get(f"{HS_API_AU_AO3_URL}{au_id}")
        response = json.loads(response.text)
        
        # "intro" and "works" are the two keys in the "response" dict
        # assign all found 
        self.au_name = au_id
        self.au_intro_line = response["intro"]
        self.au_story_details = response["works"]

    def get_all_metadata_for_embed_generation(self):
        """return all metadata lists and tuples to an external function"""

        return (self.au_link, self.au_name, self.au_intro_line, self.au_story_details)
            