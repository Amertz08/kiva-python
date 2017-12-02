import re
import requests

from datetime import datetime

RE_DATE = re.compile('.*_?date$')
FORMAT = '%Y-%m-%dT%H:%M:%SZ'

SEARCH_STATUS = ['fundraising', 'funded', 'in_repayment', 'paid', 'defaulted']
SEARCH_GENDER = ['male', 'female']
SEARCH_REGION = ['na', 'ca', 'sa', 'af', 'as', 'me', 'ee']
SEARCH_SORT = ['popularity', 'loan_amount', 'oldest', 'expiration', 'newest', 'amount_remaining', 'repayment_term']


class BaseAPI(object):

    def __init__(self, app_id=None, version=1):
        self.app_id = app_id
        self.version = version
        self.base_url = f'https://api.kivaws.org/v{self.version}/'

    @staticmethod
    def _check_param(value, name, allowed=None, single=False):
        if not value:
            return ''
        bogus = None
        if isinstance(value, str):
            if value.lower() not in allowed:
                print(f'{value.lower()} not in {allowed}')
                bogus = [value]
        else:
            if single:
                raise Exception(f'{name} must be a single value, not a list')
            if allowed:
                bogus = filter(lambda x: x.lower() not in allowed, value)
            value = ','.join(value)

        if bogus:
            print(type(value))
            raise Exception(f'Invalid {name}: {", ".join(bogus)}. Must be one of {", ".join(allowed)}')
        return value

    def _make_call(self, url, key=None, method=None, args=None, params=None):
        if args is None:
            args = []

        if params is None:
            params = {}

        if self.app_id:
            params['app_id'] = self.app_id

        resp = requests.get(self.base_url + url, params=params)
        if resp.status_code != 200:
            raise requests.HTTPError(f'Non 200 code {resp.status_code} {resp.json()}')
        raw = resp.json()

        data = key and raw[key] or raw
        if isinstance(data, list):
            obj = KivaList()
            for tmp in data:
                spam = KivaContainer(tmp)
                obj.append(spam)
        else:
            obj = KivaContainer(data)

        if 'paging' in raw.keys():
            page = raw['paging']['page']
            total = raw['paging']['pages']
            obj.page = page
            obj.total_pages = total
            obj.page_size = raw['paging']['page_size']
            obj.total_count = raw['paging']['total']
            obj.next_page = page < total and page + 1 or None
            obj.prev_page = page > 1 and page - 1 or None

            if method:
                if obj.next_page:
                    if isinstance(args, list):
                        qargs = args + [obj.next_page]
                        obj.get_next_page = lambda: method(*qargs)
                    else:
                        args['page'] = obj.next_page
                        obj.get_next_page = lambda: method(**args)
                else:
                    obj.get_next_page = lambda: None

                if obj.prev_page:
                    if isinstance(args, list):
                        qargs = args + [obj.prev_page]
                        obj.get_previous_page = lambda: method(*qargs)
                    else:
                        args['page'] = obj.prev_page
                        obj.get_previous_page = lambda: method(**args)

                else:
                    obj.get_previous_page = lambda: None
        return obj


class KivaContainer(object):
    def __init__(self, data=None):
        self.index = 0
        if data:
            self.parse(data)

    def parse(self, data):
        for key in data.keys():
            value = data[key]
            if isinstance(value, dict):
                param = KivaContainer(value)
            elif RE_DATE.match(key):
                param = datetime.strptime(value, FORMAT)
            else:
                param = value
            self.__setattr__(key, param)

    def __repr__(self):
        return str(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def keys(self):
        return self.__dict__.keys()


class KivaList(list, object):
    pass