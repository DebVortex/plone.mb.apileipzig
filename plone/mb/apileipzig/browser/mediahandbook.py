# encoding: utf-8
# zope imports
from zope.interface import implements

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

try:
    from zope.component import getUtility
except ImportError:
    from zope.app.component import getUtitlity 

# plone imports
from plone.registry.interfaces import IRegistry
from plone.memoize.interfaces import ICacheChooser

# python imports
from dedun.resources import MediahandbookCompanies
from urllib2 import HTTPError
import time

# local imports
from plone.mb.apileipzig.browser.interfaces import IMediaHandbook
from plone.mb.apileipzig.browser.controlpanel import IAPILeipzigSettings

class MediaHandbookView(BrowserView):
    """
    """
    implements(IMediaHandbook)

    index = ViewPageTemplateFile("mediahandbook.pt")

    def __init__(self, context, request):
        """
        """
        self.context = context
        self.request = request
        self.working = False
        self.object_information = False
        self.alphabetical_sorted_dict = {
            '0-9': [], 'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [],
            'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [],
            'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
            'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': [],
            'andere...': []
        }
        self.requested_companies = self.request.get('companies_with')
        self.requested_company_id = self.request.get('company_id')
        self.companies = None
        self.company = None

    def __call__(self):
        """
        """
        (self.mediahandbook, self.companies) = self.get_mediahandbook_from_api_or_cache()
        if not self.companies:
            return self.index()
        self.working = True
        self.build_alphabetical_sorted_dict(self.companies)
        self.build_link_list()
        if self.requested_company_id:
            company = selfmediahandbook.get(id=self.requested_company_id)
            self.company = {'title': company.name,
                'street_and_housenumber': self.build_street_and_housenumber(company),
                'postcode_and_city': self.build_postcode_and_city(company),
                'phone': company.phone_primary,
                'fax': company.fax_primary,
                'mailto': self.build_mailto(company),
                'email': company.email_primary,
                'website': company.url_primary,
            }
            return self.index()
        if self.requested_companies:
            self.companies_to_show =\
                self.alphabetical_sorted_dict[self.requested_companies]
        else:
            self.companies_to_show =\
                self.alphabetical_sorted_dict['0-9']
        self.companies = self.build_company_list(self.companies_to_show)
        return self.index()

    def get_companies(self):
        """ return all companies, listed in the mediahandbook
        """
        settings = getUtility(IRegistry).forInterface(IAPILeipzigSettings)
        personal_api_key = settings.api_key
        if personal_api_key:
            try:
                mediahandbook = MediahandbookCompanies(api_key=personal_api_key)
                companies = mediahandbook.all()
            except HTTPError, e:
                return
            return (mediahandbook, companies)

    def build_alphabetical_sorted_dict(self, companies):
        """
        """
        for company in companies:
            start_char = company.name[:1].upper()
            if start_char in [str(a) for a in range(10)]:
                self.alphabetical_sorted_dict['0-9'].append(company)
            elif start_char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                self.alphabetical_sorted_dict[start_char].append(company)
            else:
                self.alphabetical_sorted_dict['andere...'].append(company)

    def build_link_list(self):
        """
        """
        sort_order = ['0-9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
            'X', 'Y', 'Z', 'andere...']
        self.link_list = list()
        for key in sort_order:
            url = self.context.absolute_url() + "?companies_with=" + key
            linkdict = {'symbol': key, 'url': url}
            self.link_list.append(linkdict)

    def build_company_list(self, companies_to_show):
        """
        """
        companies = list()
        for company in companies_to_show:
            company_dict = {'title': company.name, 
                'link': self.build_company_link(company)}
            companies.append(company_dict)
        return companies

    def build_company_link(self, company):
        """
        """
        return self.context.absolute_url() + '?company_id=' + str(company.id)

    def build_postcode_and_city(self, company):
        """
        """
        city = ""
        if company.postcode:
            city = city + company.postcode
        if company.city:
            city = city + company.city
        return city

    def build_street_and_housenumber(self, company):
        """
        """
        street = ""
        if company.street:
            street = street + company.street
        if company.housenumber:
            street = street + str(company.housenumber)
        return street

    def build_mailto(self, company):
        """
        """
        mailto = ""
        if company.email_primary:
            mailto = "mailto:" + company.email_primary
        return mailto

    def get_mediahandbook_from_api_or_cache(self):
        """
        """
        now=time.time()

        chooser=getUtility(ICacheChooser)
        cache=chooser("apileipzig")
        cached_data=cache.get(self.context.title, None)
        if cached_data is not None:
            (timestamp, (mediahandbook, companies)) = cached_data
            if now-timestamp < self.context.cache_timeout:
                return (mediahandbook, companies)

            (mediahandbook, companies) = self.get_companies()
            cache[self.context.title] = (now + self.context.cache_timeout, 
                (mediahandbook, companies))
        (mediahandbook, companies) = self.get_companies()
        cache[self.context.title] = (now + self.context.cache_timeout, 
            (mediahandbook, companies))
        return (mediahandbook, companies)