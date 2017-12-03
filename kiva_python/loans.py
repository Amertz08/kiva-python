from .base import BaseAPI, SEARCH_GENDER, SEARCH_REGION, SEARCH_SORT, SEARCH_STATUS


class Loans(BaseAPI):

    def __init__(self, *args, **kwargs):
        super(Loans, self).__init__(*args, **kwargs)
        self.base_url += 'loans/'

    def __call__(self, loan_ids):
        """
        Returns loan data for given loan_ids
        :param loan_ids: List of loans_ids to get data for
        :returns List of loan data
        """
        if len(loan_ids) == 0 or len(loan_ids) > 10:
            raise Exception('You can request between 1 and 10 loans')
        lids = ','.join([str(i) for i in loan_ids])
        return self._call(
            url=f'{lids}.json',
            key='loans'
        )

    def journal_entries(self, loan_id, include_bulk=True, page=1):
        """

        """
        ib = include_bulk and 1 or 0
        return self._call(
            url=f'{loan_id}/journal_entries.json',
            params={
                'page': page,
                'include_bulk': ib
            },
            key='journal_entries',
            method=self.journal_entries,
            args=[loan_id, include_bulk],
        )

    def lenders(self, loan_id, page=1):
        """
        Returns list of lenders for given loan
        :param loan_id: id of loan
        :param page: page number of results
        :returns list of Lender data
        """
        return self._call(
            url=f'{loan_id}/lenders.json',
            params={'page': page},
            key='lenders',
            method=self.lenders,
            args=[loan_id],
        )

    def newest(self, page=1):
        """
        Returns list of newest loan listings
        :param page: page number of results
        :returns List of loans
        """
        return self._call(
            url='newest.json',
            key='loans',
            method=self.newest,
            params={'page': page}
        )

    def search(self, status=None, gender=None, sector=None, region=None, country_code=None, partner=None, q=None,
               sort_by=None, page=1):
        """
        Search loans
        :param status: Loan status ['fundraising', 'funded', 'in_repayment', 'paid', 'defaulted']
        :param gender: Gender of loan recipient ['male', 'female']
        :param sector: Market sector of loan
        :param region: Geogrphic region of loan ['na', 'ca', 'sa', 'af', 'as', 'me', 'ee']
        :param country_code: Country code of loan
        :param partner: Partner who helps with loan
        :param q: TODO: idk
        :param sort_by: Sort results by ['popularity', 'loan_amount', 'oldest', 'expiration', 'newest', 'amount_remaining', 'repayment_term']
        """
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
        status = self._check_param(status, 'status', SEARCH_STATUS)
        gender = self._check_param(gender, 'gender', SEARCH_GENDER)
        sector = self._check_param(sector, 'sector')
        region = self._check_param(region, 'region', SEARCH_REGION)
        country_code = self._check_param(country_code, 'country code')
        partner = self._check_param(partner, 'partner')
        q = self._check_param(q, 'search string', single=True)
        sort_by = self._check_param(sort_by, 'sort_by', SEARCH_SORT, True)

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
        return self._call(
            url='search.json',
            params=qopts,
            key='loans',
            method=self.search,
            args=opts,
        )
