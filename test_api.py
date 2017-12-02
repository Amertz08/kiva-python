import pprint
import kiva


def test_recent_lending_actions():
    results = kiva.recent_lending_actions()
    assert isinstance(results, kiva.KivaList), f'{type(results)} is not {type(kiva.KivaList)}'


def test_loans():
    loans = kiva.recent_lending_actions()
    if not loans:
        assert False, 'No loans found'
    else:
        n = 10 if len(loans) > 10 else len(loans)
        pprint.pprint(loans[:8])
        loan_ids = [entry.loan.id for entry in loans[:n]]
        results = kiva.loans(loan_ids)
        assert isinstance(results, kiva.KivaList), f'{type(results)} is not {type(kiva.KivaList)}'


def test_lender_loans():
    loans = kiva.lender_loans('metlifefoundation3229')
    assert isinstance(loans, kiva.KivaList), 'Loans should return KivaList'
    assert isinstance(loans[0], kiva.KivaContainer), 'Loan items should be KivaContainers'
    assert loans.page == 1, f'Should be on page 1: {loans.page}'
    next_loans = loans.get_next_page()
    assert next_loans.page == 2, f'Should be on page 2: {next_loans.page}'
