from .base import BaseAPI, KivaContainer, KivaList
from .lenders import Lenders
from .lending_actions import LendingActions
from .loans import Loans

__version__ = 0.1


class KivaAPI(BaseAPI):

    @property
    def lenders(self):
        return Lenders(self.app_id, self.version)

    @property
    def lending_actions(self):
        return LendingActions(self.app_id, self.version)

    @property
    def loans(self):
        return Loans(self.app_id, self.version)

    @property
    def methods(self):
        raise NotImplementedError('KivaAPI.methods not implemented')

    @property
    def my(self):
        raise NotImplementedError('KivaAPI.my not implemented')

    @property
    def partners(self):
        raise NotImplementedError('KivaAPI.partners not implemented')

    @property
    def teams(self):
        raise NotImplementedError('KivaAPI.teams not implemented')

    @property
    def templates(self):
        raise NotImplementedError('KivaAPI.templates not implemented')

# TODO: cannot find on API docs
# def entry_comments(entry_id, page=1):
#     return __make_call(f'journal_entries/{entry_id}/comments.json', 'comments',
#                        entry_comments, [entry_id], {'page': page})
