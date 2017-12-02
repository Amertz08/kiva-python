from .base import BaseAPI
from .lending_actions import LendingActions

__version__ = 0.1


class KivaAPI(BaseAPI):

    @property
    def lenders(self):
        return ''

    @property
    def lending_actions(self):
        return LendingActions()

    @property
    def loans(self):
        return ''

    @property
    def methods(self):
        return ''

    @property
    def my(self):
        return ''

    @property
    def partners(self):
        return ''

    @property
    def teams(self):
        return ''

    @property
    def templates(self):
        return ''


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

