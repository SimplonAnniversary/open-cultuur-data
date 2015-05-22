from datetime import datetime
from ocd_backend.log import get_source_logger
from ocd_backend.items import BaseItem

log = get_source_logger('loader')


class ArchiefAlkmaarBondaItem(BaseItem):
    namespaces = {
        'oai': 'http://www.openarchives.org/OAI/2.0/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        'xml': 'http://www.w3.org/XML/1998/namespace',
        'europeana': 'http://www.europeana.eu/schemas/ese/'
    }

    media_mime_types = {
        'webm': 'video/webm',
        'ogv': 'video/ogg',
        'ogg': 'audio/ogg',
        'mp4': 'video/mp4',
        'm3u8': 'application/x-mpegURL',
        'ts': 'video/MP2T',
        'mpeg': 'video/mpeg',
        'mpg': 'video/mpeg',
        'png': 'image/png',
        'jpg': 'image/jpeg'
    }

    def _get_text_or_none(self, xpath_expression):
        node = self.original_item.find(xpath_expression, namespaces=self.namespaces)
        if node is not None and node.text is not None:
            return unicode(node.text)

        return None

    def get_original_object_id(self):
        return self._get_text_or_none('.//oai:header/oai:identifier')

    def get_original_object_urls(self):
        original_id = self.get_original_object_id()
        return {
            'html': 'http://www.regionaalarchiefalkmaar.nl/beeldbank/%s/' % original_id.split(':')[1],
            'xml': 'https://maior.memorix.nl/api/oai/raa/key/Bonda/?verb=GetRecord&identifier=%s&metadataPrefix=ese' % original_id
        }

        #"http://www.regionaalarchiefalkmaar.nl/beeldbank/ca5efe9b-7565-403f-bdeb-54b4cb42a37b" 

    def get_rights(self):
        return u'Creative Commons Attribution-ShareAlike'

    def get_collection(self):
        return u'Archief Alkmaar Bonda'

    def get_combined_index_data(self):
        combined_index_data = {}

        title = self._get_text_or_none('.//dc:title')
        combined_index_data['title'] = title

        description = self._get_text_or_none('.//dc:description')
        if description:
            combined_index_data['description'] = description

        date = self._get_text_or_none('.//dc:date')
        if date:
            combined_index_data['date'] = datetime.strptime(self._get_text_or_none('.//dc:date'),
                                                            '%Y-%m-%d')
        combined_index_data['date_granularity'] = 8

        authors = self._get_text_or_none('.//dc:creator')
        if authors:
            combined_index_data['authors'] = [authors]

        
        media = self._get_text_or_none('.//europeana:isShownBy')

        if media:
            combined_index_data['media_urls'] = [{
                'original_url': medium.text,
                'content_type': 'image/jpeg'
            }]

        return combined_index_data

    def get_index_data(self):
        return {}

    def get_all_text(self):
        text_items = []

        # Title
        text_items.append(self._get_text_or_none('.//oi:title[@xml:lang="nl"]'))

        # Alternative title
        text_items.append(self._get_text_or_none('.//oi:alternative[@xml:lang="nl"]'))

        # Creator
        text_items.append(self._get_text_or_none('.//oi:creator[@xml:lang="nl"]'))

        # Subject
        subjects = self.original_item.findall('.//oi:subject[@xml:lang="nl"]',
                                              namespaces=self.namespaces)
        for subject in subjects:
            text_items.append(unicode(subject.text))

        # Description
        text_items.append(self._get_text_or_none('.//oi:description[@xml:lang="nl"]'))

        # Abstract
        text_items.append(self._get_text_or_none('.//oi:abstract[@xml:lang="nl"]'))

        # Publisher
        text_items.append(self._get_text_or_none('.//oi:publisher[@xml:lang="nl"]'))

        # Contributor
        contributors = self.original_item.xpath('.//oi:contributor[not(@xml:lang="en")]',
                                              namespaces=self.namespaces)
        for contributor in contributors:
            text_items.append(unicode(contributor.text))

        # Identifier
        text_items.append(self._get_text_or_none('.//oi:identifier'))

        # Source
        text_items.append(self._get_text_or_none('.//oi:source[@xml:lang="nl"]'))

        # References
        text_items.append(self._get_text_or_none('.//oi:references[@xml:lang="nl"]'))

        # Spatial
        spatial = self.original_item.xpath('.//oi:contributor[@xml:lang="nl"]',
                                           namespaces=self.namespaces)
        for place in spatial:
            text_items.append(unicode(place.text))

        # Type
        text_items.append(self._get_text_or_none('.//oi:type'))

        return u' '.join([ti for ti in text_items if ti is not None])


