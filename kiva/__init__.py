from .base import BaseAPI, KivaContainer, KivaList
from .lenders import Lenders
from .lending_actions import LendingActions
from .loans import Loans

__version__ = 0.1


class KivaAPI(BaseAPI):

    @property
    def lenders(self):
        return Lenders(self.version)

    @property
    def lending_actions(self):
        return LendingActions(self.version)

    @property
    def loans(self):
        return Loans(self.version)

    @property
    def methods(self):
        return ''

    @property
    def my(self):
        return ''

    @property
    def partners(self):
        return ''

    @property
    def teams(self):
        return ''

    @property
    def templates(self):
        return ''

# TODO: cannot find on API docs
# def entry_comments(entry_id, page=1):
#     return __make_call(f'journal_entries/{entry_id}/comments.json', 'comments',
#                        entry_comments, [entry_id], {'page': page})

