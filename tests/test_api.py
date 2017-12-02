import pytest
import pprint

from kiva import KivaAPI, KivaList, KivaContainer


@pytest.fixture
def api():
    return KivaAPI()


def test_recent_lending_actions(api):
    results = api.lending_actions.recent()
    assert isinstance(results, KivaList), f'{type(results)} is not {type(KivaList)}'


def test_loans(api):
    loans = api.lending_actions.recent()
    if not loans:
        assert False, 'No loans found'
    else:
        n = 10 if len(loans) > 10 else len(loans)
        pprint.pprint(loans[:n])
        loan_ids = [entry.loan.id for entry in loans[:n]]
        results = api.loans(loan_ids)
        assert isinstance(results, KivaList), f'{type(results)} is not {type(KivaList)}'


def test_lender_loans(api):
    loans = api.lenders.loans('metlifefoundation3229')
    assert isinstance(loans, KivaList), 'Loans should return KivaList'
    assert isinstance(loans[0], KivaContainer), 'Loan items should be KivaContainers'
    assert loans.page == 1, f'Should be on page 1: {loans.page}'
    next_loans = loans.get_next_page()
    assert next_loans.page == 2, f'Should be on page 2: {next_loans.page}'
