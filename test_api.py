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
        loan_ids = [entry.loan.id for entry in loans]
        results = kiva.loans(loan_ids[:n])
        assert isinstance(results, kiva.KivaList), f'{type(results)} is not {type(kiva.KivaList)}'

