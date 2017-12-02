import re
import requests

from datetime import datetime

__version__ = 0.1

API_VERSION = 1

RE_DATE = re.compile('.*_?date$')
BASE_URL = 'http://api.kivaws.org/v%i/' % API_VERSION
FORMAT = '%Y-%m-%dT%H:%M:%SZ'

SEARCH_STATUS = ['fundraising', 'funded', 'in_repayment', 'paid', 'defaulted']
SEARCH_GENDER = ['male', 'female']
SEARCH_REGION = ['na', 'ca', 'sa', 'af', 'as', 'me', 'ee']
SEARCH_SORT = ['popularity', 'loan_amount', 'oldest', 'expiration', 'newest', 'amount_remaining', 'repayment_term']


def recent_lending_actions():
    return __make_call('lending_actions/recent.json', 'lending_actions')


def lender_info(lender_ids):
    # need one lender, can have up to 50
    if len(lender_ids) == 0:
        raise Exception('Must have at least 1 lender id')
    elif len(lender_ids) > 50:
        raise Exception(f'Can have up to 50 lender ids; {len(lender_ids)} submitted')

    lids = ','.join([str(i) for i in lender_ids])

    return __make_call(f'lenders/{lids}.json', 'lenders')


def lender_loans(lender_id, page=1):
    params = {'page': page}
    return __make_call(
        url=f'lenders/{lender_id}/loans.json',
        key='loans',
        method=lender_loans,
        args=[lender_id],
        params=params
    )


def newest_loans(page=1):
    return __make_call('loans/newest.json', 'loans', newest_loans, params={'page': page})


def loans(loan_ids):
    if len(loan_ids) == 0 or len(loan_ids) > 10:
        raise Exception('You can request between 1 and 10 loans')
    lids = ','.join([str(i) for i in loan_ids])

    return __make_call(f'loans/{lids}.json', 'loans')


def lenders(loan_id, page=1):
    return __make_call(f'loans/{loan_id}/lenders.json', 'lenders', lenders, [loan_id], {'page': page})


def journal_entries(loan_id, include_bulk=True, page=1):
    ib = include_bulk and 1 or 0
    params = {
        'page': page,
        'include_bulk': ib
    }
    return __make_call(f'loans/{loan_id}/journal_entries.json',
                       'journal_entries', journal_entries, [loan_id, include_bulk], params)


def entry_comments(entry_id, page=1):
    return __make_call(f'journal_entries/{entry_id}/comments.json', 'comments',
                       entry_comments, [entry_id], {'page': page})


def search_loans(status=None, gender=None, sector=None, region=None, country_code=None, partner=None, q=None,
                 sort_by=None, page=1):

    opts = {
        'status': status,
        'gender': gender,
        'sector': sector,
        'region': region,
        'country_code': country_code,
        'partner': partner,
        'q': q,
        'sort_by': sort_by
    }
    
    # check params
    status = __check_param(status, 'status', SEARCH_STATUS)
    gender = __check_param(gender, 'gender', SEARCH_GENDER)
    sector = __check_param(sector, 'sector')
    region = __check_param(region, 'region', SEARCH_REGION)
    country_code = __check_param(country_code, 'country code')
    partner = __check_param(partner, 'partner')
    q = __check_param(q, 'search string', single=True)
    sort_by = __check_param(sort_by, 'sort_by', SEARCH_SORT, True)

    qopts = {
        'status': status,
        'gender': gender,
        'sector': sector,
        'region': region,
        'country_code': country_code,
        'partner': partner,
        'q': q,
        'sort_by': sort_by,
        'page': page
    }

    for k in filter(lambda x: qopts[x] == '', qopts):
        del qopts[k]
    url = 'loans/search.json'
    return __make_call(url, 'loans', search_loans, opts, qopts)
    

def __check_param(value, name, allowed=None, single=False):
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


def __make_call(url, key=None, method=None, args=None, params=None):
    if args is None:
        args = []

    resp = requests.get(BASE_URL + url, params=params)
    if resp.status_code != 200:
        raise requests.HTTPError(f'Non 200 code: {resp.status_code}')
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
        current = raw['paging']['page']
        total = raw['paging']['pages']
        obj.current_page = current
        obj.total_pages = total
        obj.page_size = raw['paging']['page_size']
        obj.total_count = raw['paging']['total']
        obj.next_page = current < total and current +1 or None
        obj.prev_page = current > 1 and current - 1 or None

        if method:
            if obj.next_page:
                if isinstance(args, list):
                    qargs = args+[obj.next_page]
                    obj.getNextPage = lambda: method(*qargs)
                else:
                    args['page'] = obj.next_page
                    obj.getNextPage = lambda: method(**args)
            else:
                obj.getNextPage = lambda: None

            if obj.prev_page:
                if isinstance(args, list):
                    qargs = args+[obj.prev_page]
                    obj.getPreviousPage = lambda: method(*qargs)
                else:
                    args['page'] = obj.prev_page
                    obj.getPreviousPage = lambda: method(**args)

            else:
                obj.getPreviousPage = lambda: None
    
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
