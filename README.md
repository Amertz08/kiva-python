kiva-python
===========

```Python
from kiva import KivaAPI

api = KivaAPI('com.example')

# loans endpoints
loans = api.loans([1, 2, 3])
loans.page

next_loans = loans.next_page
loans = next_loans.prev_page

loan_lenders = api.loans.lenders(123)

newest_loans = api.loans.newest()

# Lender endpoints
lenders = api.lenders([1, 2, 3])
lender_loans = api.lenders.loans(1)
```
