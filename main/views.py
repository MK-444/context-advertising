import logging
from typing import List, Set, Dict

from django.shortcuts import render
from django.views import View
from bs4 import BeautifulSoup
import requests
from rake_nltk import Rake

from .models import Tag, Advert

logger = logging.getLogger(__name__)

class IndexView(View):
    """
    URL processing to find relevant ads.
    """
    def get(self, request):
        """
        Handle GET requests for the index page.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered index.html template.
        """
        return render(request, 'main/index.html')

    def post(self, request):
        """
        Handle POST requests with URL.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered index.html template with relevant ads and common tags.
        """
        url = request.POST.get('url')
        all_text = self.extract_text_from_url(url)
        keywords_extracted = self.extract_keywords(all_text)
        commonwords = self.find_common_tags(keywords_extracted)
        relevantads = self.find_relevant_ads(commonwords)
        context = {
            'relevantads': relevantads,
            'commonwords': commonwords
        }
        return render(request, 'main/index.html', context)

    def extract_text_from_url(self, url: str) -> str:
        """
        Extract text from a given URL.

        Args:
            url (str): The URL to extract text from.

        Returns:
            str: The extracted text from the URL.

        Raises:
            Exception: If an error happens during the HTTP request or parsing the HTML.
        """
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, 'html.parser')
        all_text = ''
        for para in soup.find_all('p'):
            all_text += str(para.get_text())
        return all_text

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from a given text.

        Args:
            text (str): The text to extract keywords from.

        Returns:
            List[str]: A list of extracted keywords.
        """
        rake_var = Rake()
        rake_var.extract_keywords_from_text(text)
        return rake_var.get_ranked_phrases()

    def find_common_tags(self, keywords_extracted: List[str]) -> List[str]:
        """
        Find common tags between extracted keywords and existing tags.

        Args:
            keywords_extracted (List[str]): A list of extracted keywords.

        Returns:
            List[str]: A list of common tags between extracted keywords and existing tags.
        """
        adtags = [tag.tagname for tag in Tag.objects.all()]
        common_tags = list(set(keywords_extracted) & set(adtags))
        logger.info(f"Common tags found: {', '.join(common_tags)}")
        return common_tags

    def find_relevant_ads(self, commonwords: List[str]) -> List[Advert]:
        """
        Find relevant ads based on common tags.

        Args:
            common_tags (List[str]): A list of common tags.

        Returns:
            List[Advert]: A list of relevant ads based on common tags.
        """
        relevant_ads: List[Advert] = []
        for advert in Advert.objects.all():
            for tag in advert.tags.all():
                if tag.tagname in commonwords:
                    relevant_ads.append(advert)
                    break
        logger.info(f"Relevant ads found: {len(relevant_ads)}")
        return list(set(relevant_ads))