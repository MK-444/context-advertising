from django.shortcuts import render
from django.views import View
from bs4 import BeautifulSoup
import requests
from rake_nltk import Rake
from .models import Tag, Advert


class IndexView(View):
    template_name = 'main/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        url = request.POST.get('url')
        relevant_ads = self.get_relevant_ads(url)
        context = {
            'relevantads': relevant_ads,
        }
        return render(request, self.template_name, context)

    def extract_keywords(self, text):
        rake_var = Rake()
        rake_var.extract_keywords_from_text(text)
        return rake_var.get_ranked_phrases()

    def get_relevant_ads(self, url):
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, 'html.parser')
        all_text = ''.join([str(para.get_text()) for para in soup.find_all('p')])
        keywords_extracted = self.extract_keywords(all_text)
        ad_tags = self.get_ad_tags()
        common_words = list(set(keywords_extracted) & set(ad_tags))
        relevant_ads = self.filter_ads_by_tags(common_words)
        return relevant_ads

    def get_ad_tags(self):
        return [tag.tagname for tag in Tag.objects.all()]

    def filter_ads_by_tags(self, common_words):
        relevant_ads = []
        for advert in Advert.objects.all():
            for tag in advert.tags.all():
                if tag.tagname in common_words:
                    relevant_ads.append(advert)
                    break  # No need to continue checking tags for this ad
        return relevant_ads
