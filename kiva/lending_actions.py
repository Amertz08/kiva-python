from .base import BaseAPI


class LendingActions(BaseAPI):

    def recent(self):
        return self._make_call(
            url='lending_actions/recent.json',
            key='lending_actions'
        )
