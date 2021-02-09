from functions.tmdb import SwitchCaseTmdb

    
def test_switch_get_function_tmdb_movie():
    t = SwitchCaseTmdb("movie", ['the', 'matrix'])
    assert 'The Movie DB Movie Info' in t.switch()


def test_switch_get_function_tmdb_movie_release():
    t = SwitchCaseTmdb("mr", ['lord', 'of', 'the', 'rings'])
    assert 'The Movie DB Movie Release Dates:' in t.switch()


def test_switch_get_function_tmdb_tvshow():
    t = SwitchCaseTmdb("tvshow", ['the', 'boys'])
    assert 'The Movie DB TVshow Info:' in t.switch()


def test_switch_get_function_tmdb_tvshow_release():
    t = SwitchCaseTmdb("tvr", ['big', 'bang', 'theory'])
    assert 'The Movie DB tvshow Release Dates:' in t.switch()


def test_switch_get_function_tmdb_new_tvshows():
    t = SwitchCaseTmdb("ntv", [''])
    assert 'The Movie DB New TVshow Release Dates' in t.switch()


