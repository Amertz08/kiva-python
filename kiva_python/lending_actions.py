from .base import BaseAPI


class LendingActions(BaseAPI):

    def recent(self):
        """
        Returns list of recent lender actions
        """
        return self._call(
            url='lending_actions/recent.json',
            key='lending_actions'
        )
