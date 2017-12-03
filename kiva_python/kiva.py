from .base import BaseAPI
from .lenders import Lenders
from .lending_actions import LendingActions
from .loans import Loans


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
