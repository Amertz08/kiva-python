from .base import KivaContainer, KivaList, SEARCH_STATUS, SEARCH_GENDER, SEARCH_REGION, SEARCH_SORT
from .kiva import KivaAPI

__version__ = 0.1

# TODO: cannot find on API docs
# def entry_comments(entry_id, page=1):
#     return __make_call(f'journal_entries/{entry_id}/comments.json', 'comments',
#                        entry_comments, [entry_id], {'page': page})
