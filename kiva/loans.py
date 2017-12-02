from .base import BaseAPI


class Loans(BaseAPI):

    def __call__(self, loan_ids):
        if len(loan_ids) == 0 or len(loan_ids) > 10:
            raise Exception('You can request between 1 and 10 loans')
        lids = ','.join([str(i) for i in loan_ids])
        return self._make_call(f'loans/{lids}.json', 'loans')

    def journal_entries(self, loan_id, include_bulk=True, page=1):
        ib = include_bulk and 1 or 0
        params = {
            'page': page,
            'include_bulk': ib
        }
        return self._make_call(f'loans/{loan_id}/journal_entries.json', 'journal_entries', self.journal_entries,
                               [loan_id, include_bulk], params)

    def lenders(self, loan_id, page=1):
        return self._make_call(f'loans/{loan_id}/lenders.json', 'lenders', self.lenders, [loan_id], {'page': page})

    def newest(self, page=1):
        return self._make_call('loans/newest.json', 'loans', self.newest, params={'page': page})

