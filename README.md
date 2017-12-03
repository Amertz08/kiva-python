kiva-python
===========

```Python
from kiva_python import KivaAPI

kiva = KivaAPI('com.example')

# loans endpoints
loans = kiva.loans([1, 2, 3])
loans.page

next_loans = loans.next_page
loans = next_loans.prev_page

loan_lenders = kiva.loans.lenders(123)

newest_loans = kiva.loans.newest()

# Lender endpoints
lenders = kiva.lenders([1, 2, 3])
lender_loans = kiva.lenders.loans(1)
```
