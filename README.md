kiva-python
===========

Access the Kiva API via Python

	>>> import Kiva
	>>> latest = Kiva.getNewestLoans()
	# All normal list methods work on the results.
	# Grab the first result:
	>>> l = latest[0]
	# The data will work just like a normal dictionary.
	>>> l.keys()
	['status', 'funded_amount', 'use', 'posted_date', 'basket_amount', 'name', 'sector', 'image', 'borrower_count', 'loan_amount', 'location', 'activity', 'partner_id', 'id', 'description']
	>>> l['status']
	u'fundraising'
	# I prefer object-type references, so that works, too:
	>>> l.status
	u'fundraising'
	# Dates are automatically changed to datetime objects.
	>>> l.posted_date
	datetime.datetime(2009, 4, 16, 19, 10, 8)
	>>> l.posted_date.year
	2009

	# The results act like lists, but they do a bit more.
	>>> len(latest)
	20
	>>> latest.current_page
	1
	>>> next.total_pages
	37
	>>> latest.next_page
	2
	# prev_page will return None because this is the first page
	>>> latest.prev_page
	# We can also get the next and previous set of results
	>>> next = latest.getNextPage()
	>>> next.current_page
	2

	# Searching is fairly straight forward:
	>>> s=Kiva.searchLoans(region='af')
	>>> s.total_count
	29097
	# Some search options can take a string or list of strings:
	>>> s=Kiva.searchLoans(region=['af', 'as'])
	>>> s.total_count
	61121
	# Basic parameter checking:
	>>> s=Kiva.searchLoans(region='nope')

	Traceback (most recent call last):
	  File "<pyshell#38>", line 1, in <module>
	    s=Kiva.searchLoans(region='nope')
	  File "c:/projects/kiva-python/trunk\Kiva.py", line 77, in searchLoans
	    region       = __check_param(region,       'region', SEARCH_REGION)
	  File "c:/projects/kiva-python/trunk\Kiva.py", line 109, in __check_param
	    (name, ", ".join(bogus), ", ".join(allowed)))
	Exception: Invalid region: nope. Must be one of na, ca, sa, af, as, me, ee
	>>> 