from .base import BaseAPI
from .lenders import Lenders
from .lending_actions import LendingActions
from .loans import Loans

__version__ = 0.1


class KivaAPI(BaseAPI):

    @property
    def lenders(self):
        return Lenders(self.version)

    @property
    def lending_actions(self):
        return LendingActions(self.version)

    @property
    def loans(self):
        return Loans(self.version)

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

# TODO: cannot find on API docs
# def entry_comments(entry_id, page=1):
#     return __make_call(f'journal_entries/{entry_id}/comments.json', 'comments',
#                        entry_comments, [entry_id], {'page': page})


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

