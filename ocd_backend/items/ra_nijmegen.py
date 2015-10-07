from datetime import datetime
import re

import requests

from ocd_backend.items import BaseItem
from ocd_backend.utils.misc import parse_date
from ocd_backend.extractors import HttpRequestMixin


class NijmegenGrintenItem(BaseItem):
    def get_original_object_id(self):
        return unicode(self.original_item['identificatie'])

    def get_original_object_urls(self):
        objnr = unicode(self.get_original_object_id())
        return {
            'html': unicode(
                self.original_item['detailpagina digitale studiezaal']),
        }

    def get_collection(self):
        return u'%s - %s' % (
            self.original_item['instelling'], self.original_item['collectie'])

    def get_rights(self):
        return unicode(self.original_item['auteursrecht foto'])

    def _get_date_and_granularity(self):
        earliest_date = self.original_item.get(
            'Vroegst mogelijke datering', None)
        if earliest_date is not None:
            if len(earliest_date) > 4:
                datesplit = earliest_date.split("/")
                if len(datesplit) > 2:
                    return 8, datetime(int(datesplit[2]), int(datesplit[1]), int(datesplit[0]))
                else:
                    return 6, datetime(int(datesplit[1]), int(datesplit[0]), 1)
            else:
                return 4, datetime(int(earliest_date), 1, 1)
        else:
            return 16, None

    def _get_image_link(self):
        return self.original_item['link foto']

    def get_combined_index_data(self):
        index_data = {}
        index_data['title'] = unicode(self.original_item.get('adres', ''))

        gran, date = self._get_date_and_granularity()
        if gran and date:
            index_data['date_granularity'] = gran
            index_data['date'] = date

        desc = self.original_item.get("beschrijving", None)
        if desc is not None:
            index_data['description'] = unicode(desc)

        # author is optional
        index_data['authors'] = [unicode(self.original_item["auteur"])]

        # get jpeg images from static host
        img_url = self._get_image_link()
        if img_url is not None:
            index_data['media_urls'] = [{
                'original_url': img_url,
                'content_type': 'image/jpeg'}]
        else:
            index_data['media_urls'] = []

        index_data['all_text'] = self.get_all_text()

        return index_data

    def get_index_data(self):
        index_data = {}
        return index_data

    def get_all_text(self):
        # all text consists of a simple space concatenation of the fields
        fields = [
            'adres', 'plaatsnaam', 'vroegst', 'instelling', 'collectie',
            'documenttype', 'trefwoord', 'auteur', 'laatst', 'beschrijving',
            'auteursrechthouder', 'rubriek', 'wijk']

        text = u' '.join(
            [unicode(self.original_item.get(f, '')) for f in fields])

        return unicode(text)


class NijmegenDoornroosjeItem(BaseItem):
    def get_original_object_id(self):
        return unicode(self.original_item['documentnummer'])

    def get_original_object_urls(self):
        objnr = unicode(self.get_original_object_id())
        return {
            'html': unicode(
                self.original_item['url detailpagina']),
        }

    def get_collection(self):
        return u'%s - %s' % (
            self.original_item['instelling'], self.original_item['collectie'])

    def get_rights(self):
        return u'https://creativecommons.org/licenses/by-sa/3.0/'

    def _get_date_and_granularity(self):
        earliest_date = self.original_item.get(
            'Vroegst mogelijke datering', None)
        if earliest_date is not None:
            if len(earliest_date) > 4:
                datesplit = earliest_date.split("/")
                if len(datesplit) > 2:
                    return 8, datetime(int(datesplit[2]), int(datesplit[1]), int(datesplit[0]))
                else:
                    return 6, datetime(int(datesplit[1]), int(datesplit[0]), 1)
            else:
                return 4, datetime(int(earliest_date), 1, 1)
        else:
            return 16, None

    def _get_image_link(self):
        return self.original_item['url afbeelding']

    def get_combined_index_data(self):
        index_data = {}
        index_data['title'] = unicode(
            self.original_item.get('beschrijving', ''))

        gran, date = self._get_date_and_granularity()
        if gran and date:
            index_data['date_granularity'] = gran
            index_data['date'] = date

        desc = self.original_item.get("beschrijving", None)
        if desc is not None:
            index_data['description'] = unicode(desc)

        # author is optional
        index_data['authors'] = [unicode(self.original_item["Auteur"])]

        # get jpeg images from static host
        img_url = self._get_image_link()
        if img_url is not None:
            index_data['media_urls'] = [{
                'original_url': img_url,
                'content_type': 'image/jpeg'}]
        else:
            index_data['media_urls'] = []

        index_data['all_text'] = self.get_all_text()

        return index_data

    def get_index_data(self):
        index_data = {}
        return index_data

    def get_all_text(self):
        # all text consists of a simple space concatenation of the fields
        fields = [
            'beginjaar', 'instelling', 'collectie',
            'Auteur', 'gemeente', 'beschrijving',
            'type', 'eindjaar']

        text = u' '.join(
            [unicode(self.original_item.get(f, '')) for f in fields])

        return unicode(text)


class NijmegenVierdaagseItem(BaseItem, HttpRequestMixin):
    def get_original_object_id(self):
        return unicode(self.original_item['Identificatie'])

    def get_original_object_urls(self):
        objnr = unicode(self.get_original_object_id())
        return {
            'html': unicode(
                self.original_item['Url detailpagina']),
        }

    def get_collection(self):
        return u'%s - %s' % (
            self.original_item['Instelling'], self.original_item['Collectie'])

    def get_rights(self):
        return u'https://creativecommons.org/licenses/by-sa/3.0/'

    def _get_date_and_granularity(self):
        earliest_date = self.original_item.get(
            'Vroegst mogelijke datering', None)
        if earliest_date is not None:
            if len(earliest_date) > 4:
                datesplit = earliest_date.split("/")
                if len(datesplit) > 2:
                    return 8, datetime(int(datesplit[2]), int(datesplit[1]), int(datesplit[0]))
                else:
                    return 6, datetime(int(datesplit[1]), int(datesplit[0]), 1)
            else:
                return 4, datetime(int(earliest_date), 1, 1)
        else:
            return 16, None

    def _get_image_link(self):
        obj_id = self.get_original_object_id()
        req = self.http_session.get(u'http://www.nijmegen.nl/opendata/archief/%s.jpg' % (
            obj_id))
        headers = req.headers
        if headers['content-type'] == 'image/jpeg':
            return u'http://www.nijmegen.nl/opendata/archief/%s.jpg' % (
                obj_id)

    def get_combined_index_data(self):
        index_data = {}
        index_data['title'] = unicode(
            self.original_item.get('Beschrijving', ''))

        gran, date = self._get_date_and_granularity()
        if gran and date:
            index_data['date_granularity'] = gran
            index_data['date'] = date

        desc = self.original_item.get("Beschrijving", None)
        if desc is not None:
            index_data['description'] = unicode(desc)

        # author is optional
        index_data['authors'] = [unicode(self.original_item["Auteur"])]

        # get jpeg images from static host
        img_url = self._get_image_link()
        if img_url is not None:
            index_data['media_urls'] = [{
                'original_url': img_url,
                'content_type': 'image/jpeg'}]
        else:
            index_data['media_urls'] = []

        index_data['all_text'] = self.get_all_text()

        return index_data

    def get_index_data(self):
        index_data = {}
        return index_data

    def get_all_text(self):
        # all text consists of a simple space concatenation of the fields
        fields = [
            'Omschrijving locatie', 'Plaatsnaam', 'Wijknaam (Nijmegen)',
            'Auteur', 'Instelling', 'Collectie', 'Straatnaam', 'Trefwoord',
            'Documenttype', 'Beschrijving', 'Auteursrechthouder',
            'Vroegst mogelijke datering']

        text = u' '.join(
            [unicode(self.original_item.get(f, '')) for f in fields])

        return unicode(text)
