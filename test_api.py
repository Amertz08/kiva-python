import kiva


def test_recent_lending_actions():
    results = kiva.recent_lending_actions()
    assert isinstance(results, kiva.KivaList), f'{type(results)} is not {type(kiva.KivaList)}'
