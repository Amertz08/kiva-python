from .base import BaseAPI


class Lenders(BaseAPI):

    def __init__(self, *args, **kwargs):
        super(Lenders, self).__init__(*args, **kwargs)
        self.base_url += 'lenders/'

    def __call__(self, lender_ids):
        """
        Gets the lenders with the given IDs
        :param lender_ids: List of lender ids to get data for
        :return list of lender data
        """
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
        """
        Returns list of loans for given lender_id
        :param lender_id: Lender ID to get loans for
        :param page: page of results
        :returns List of loans lent by given lender
        """
        return self._make_call(
            url=f'{lender_id}/loans.json',
            params={'page': page}
            key='loans',
            method=self.loans,
            args=[lender_id],
        )
