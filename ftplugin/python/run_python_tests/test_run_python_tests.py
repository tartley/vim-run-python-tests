# Run these tests by running this from your home dir:
#
#   vim -c "execute 'pyfile .vim/ftplugin/python/run_python_tests/test_run_python_tests.py' | q" dummy.py
#
# This will print nothing and exit if all tests pass, or display just the
# first traceback and wait for ENTER if any tests fail.
#
# It uses 'execute' instead of 'pyfile' directly, because that allows us to
# chain a list of commands, separated by |, so that a succesful run will
# quit (the 'q'). (pyfile by itself would eat the whole line as a filename)
#
# Methods and classes under test are imported by the command-line above
# specifying a python file (dummy.py) to edit, so all python plugins
# (including the one we are testing) are imported by Vim at startup.


from contextlib import contextmanager
from inspect import isfunction
import os
import sys

from mock import patch


@contextmanager
def assertRaises(expectedType=None):
    try:
        yield
    except Exception, e:
        if expectedType:
            if not isinstance(e, expectedType):
                msg = 'Expecting %s, got %s: %s' % (
                    expectedType.__name__, type(e).__name__, str(e))
                raise AssertionError(msg)
    else:
        name = expectedType.__name__ if expectedType else 'assertion'
        raise AssertionError("Expecting %s, didn't raise" % (name,))


def test_normalise():
    assert _normalise('/Test/') == '/Test'


def test_dirnameconvention_is_test():
    assert _DirnameConvention('test').is_test('hello') == False
    assert _DirnameConvention('test').is_test('hello_test') == False
    assert _DirnameConvention('Test').is_test('hello/test')
    assert _DirnameConvention('test').is_test('hello/Test/')

def test_dirnameconvention_to_product():
    assert _DirnameConvention('test').to_product('hello/Test') == 'hello'
    assert _DirnameConvention('Test').to_product('hello/test') == 'hello'
    assert _DirnameConvention('Test').to_product('hello/test/') == 'hello'
    with assertRaises(RuntimeError):
        _DirnameConvention('test').to_product('hello/tes')

def test_dirnameconvention_to_test():
    assert _DirnameConvention('test').to_test('hello') == \
        os.sep.join(['hello', 'test'])
    assert _DirnameConvention('test').to_test('hello/') == \
        os.sep.join(['hello', 'test'])
    with assertRaises(RuntimeError):
        _DirnameConvention('Test').to_test('hello/test')
    with assertRaises(RuntimeError):
        _DirnameConvention('test').to_test('hello/Test')
    with assertRaises(RuntimeError):
        _DirnameConvention('test').to_test('hello/Test/')


def test_filenameconvention_is_test():
    assert _FilenameConvention('Test_*').is_test('test_hello')
    assert _FilenameConvention('test_*').is_test('Test_hello')
    assert _FilenameConvention('test_*').is_test('stest_hello') == False

    assert _FilenameConvention('*_Test').is_test('hello_test')
    assert _FilenameConvention('*_test').is_test('hello_Test')
    assert _FilenameConvention('*_test').is_test('hello_tests') == False

def test_filenameconvention_to_product():
    assert _FilenameConvention('*_test').to_product('hello_Test') == 'hello'
    assert _FilenameConvention('*_Test').to_product('hello_test') == 'hello'
    with assertRaises(RuntimeError):
        _FilenameConvention('Test_*').to_product('hello')

def test_filenameconvention_to_test():
    assert _FilenameConvention('*_Test').to_test('hello') == 'hello_Test'
    assert _FilenameConvention('Test_*').to_test('hello') == 'Test_hello'
    with assertRaises(RuntimeError):
        _FilenameConvention('Test_*').to_test('Test_hello')


def test_get_filename_components():
    assert _get_filename_components(r'C:\d1\d2\file.ext') == \
        (r'C:\d1\d2', 'file', '.ext')
    assert _get_filename_components(r'd2\file.ext') == \
        (r'd2', 'file', '.ext')
    assert _get_filename_components(r'file.ext') == ('', 'file', '.ext')



@patch('os.path.isfile')
def assert_get_test_filename_finds(filename, expected, mock_isfile):
    mock_isfile.side_effect = lambda f: f == expected
    assert _find_test(filename) == expected


def test_get_test_filename():
    # look for a test file in 'unittests' subdir
    assert_get_test_filename_finds(
        os.path.join('p1', 'f1.py'),
        os.path.join('p1', 'unittests', 'f1-tests.py')
    )
    # look for a test file in the same dir
    assert_get_test_filename_finds(
        os.path.join('p1', 'f1.py'),
        os.path.join('p1', 'f1-tests.py')
    )



@patch('os.path.isfile')
def assert_get_product_filename_finds(filename, expected, mock_isfile):
    mock_isfile.side_effect = lambda f: f == expected
    assert _find_product(filename) == expected


def test_get_product_filename():
    # look for product file outside of 'unittest' directory
    assert_get_product_filename_finds(
        os.path.join('p1', 'unittest', 'test-f1.py'),
        os.path.join('p1', 'f1.py')
    )
    # look for product file in the same directory
    assert_get_product_filename_finds(
        os.path.join('p1', 'test-f1.py'),
        os.path.join('p1', 'f1.py')
    )



def main():
    # run all 'test_' functions in this file
    test_funcs = [
        (name, func)
        for name, func in sys.modules['__main__'].__dict__.items()
        if name.startswith('test_') and isfunction(func)
    ]
    for name, func in test_funcs:
        func()



if __name__ == '__main__':
    main()

