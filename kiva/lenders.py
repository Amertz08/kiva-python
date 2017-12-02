from .base import BaseAPI


class Lenders(BaseAPI):

    def __init__(self, *args, **kwargs):
        super(Lenders, self).__init__(*args, **kwargs)
        self.base_url += 'lenders/'

    def __call__(self, lender_ids):
        # need one lender, can have up to 50
        if len(lender_ids) == 0:
            raise Exception('Must have at least 1 lender id')
        elif len(lender_ids) > 50:
            raise Exception(f'Can have up to 50 lender ids; {len(lender_ids)} submitted')

        lids = ','.join([str(i) for i in lender_ids])

        return self._make_call(
            url=f'{lids}.json',
            key='lenders'
        )

    def loans(self, lender_id, page=1):
        params = {'page': page}
        return self._make_call(
            url=f'{lender_id}/loans.json',
            params=params
            key='loans',
            method=self.loans,
            args=[lender_id],
        )
