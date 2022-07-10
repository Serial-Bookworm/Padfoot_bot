import re
from botutils.constants import FFN_AUTHOR_CHECK_STR, HS_API_AU_FFN_URL
from bs4 import BeautifulSoup
import requests
import json

class FFNAuProfiler:
    def __init__(self, msg) -> None:
        self.message = msg
        self.au_link = None
        self.au_name = None
        self.au_intro_line = None
        self.au_story_names_ids_tuple = None
        self.au_story_details = None

        # start the au profile crawl
        self._execute_au_crawl()

    def _execute_au_crawl(self):
        self._fetch_au_link_from_message()
        self._crawl_au_profile_ffn()

    def _fetch_au_link_from_message(self):
        """extract author profile ffn link from message text"""
        try:
            all_links = re.findall(r'(https?://[^\s]+)', self.message)
            all_links_to_get_profiles_for = []
            for link in all_links:
                if FFN_AUTHOR_CHECK_STR in link:
                    all_links_to_get_profiles_for.append(link)
                    break # get only the first profile link
        
            self.au_link = all_links_to_get_profiles_for[0]
        except:
            print("No ffn au link found.")

    def _crawl_au_profile_ffn(self):
        """to crawl au profile link fetched"""
        
        link = self.au_link
        try:
            au_id = link[link.index('u/')+2 : link.index('/', link.index('u/')+4)]
        except:
            au_id = link[link.index('u/')+2 :]
        
        response = requests.get(f"{HS_API_AU_FFN_URL}{au_id}")
        response = json.loads(response.text)

        # crawl html
        soup = BeautifulSoup(response, "html.parser")

        # name of the author
        name = soup.find("div", attrs={'id': 'content_wrapper_inner'}).find("span").text.strip()

        raw_bio = soup.find('div', attrs={'id': 'bio'})
        
        # full_profile_bio = raw_bio.text # this is often too long, so skipping it for now.
        intro_line_bio =  raw_bio.find('div').text # this is enough

        all_stories_raw = soup.find('div', attrs={'id': "st_inside"})
        all_stories_details = all_stories_raw.find_all('div', attrs={'class': 'z-indent z-padtop'})
        all_stories_details_text = [] 
        for story in all_stories_details:
            all_stories_details_text.append(story.text)
        
        all_stories_names_soup = all_stories_raw.find_all('div', attrs={'class': 'z-list mystories'})
        all_stories_names_ids_tuple = []
        for name_soup in all_stories_names_soup:
            namestr = name_soup['data-title']
            namestr_decoded = bytes(namestr, "utf-8").decode("unicode_escape")
            storyid = name_soup['data-storyid']
            all_stories_names_ids_tuple.append((namestr_decoded, storyid))
        
        # assign all found 
        self.au_name = name
        self.au_intro_line = intro_line_bio
        self.au_story_details = all_stories_details_text
        self.au_story_names_ids_tuple = all_stories_names_ids_tuple

    def get_all_metadata_for_embed_generation(self):
        """return all metadata lists and tuples to an external function"""

        return (self.au_link, self.au_name, self.au_intro_line, self.au_story_names_ids_tuple, self.au_story_details)
            