from .base import BaseAPI


class LendingActions(BaseAPI):

    def recent(self):
        return self._make_call('lending_actions/recent.json', 'lending_actions')
