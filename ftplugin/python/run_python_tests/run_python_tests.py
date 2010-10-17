from fnmatch import fnmatch
import os
from os.path import (
    basename, dirname, isdir, join, relpath, sep, split, splitdrive,
    splitext,
)
import re
import vim

# -- public ----

# All possible unit test subdirectory naming conventions
# (the possibility that tests reside in the same directory as product code
# is implicitly considered, and need not be listed here)
# Matching is case-insensitive.
test_subdir_names = [ 'tests', 'test', 'unittest', 'unittests', ]

# All possible unit test file naming conventions
# Order is important. 'test*' would erroneously match even when the user had
# named their files 'test_*'. Hence 'test*' should come afterwards.
# Matching is case-insensitive.
test_filenames = [
    'test_*', 'test-*', 'test*',
    '*_test', '*-test', '*test',
    '*_tests', '*-tests', '*tests',
]

# the preferred conventions to use when creating new test files,
# expressed as indices into the above lists
preferred_subdir = 0
preferred_filename = 0


def toggle_test(create=False):
    '''
    If current file has unit tests, open them. If current file is a unit test,
    open the corresponding product module.
    '''
    if vim.current.buffer.name is None:
        print 'Not a file'
        return

    current = vim.current.buffer.name
    test = _find_test(current)
    if test:
        vim.command('hide edit %s' % (relpath(test),))
    else:
        if _looks_like_test(current):
            product = _find_product(current)
            if product:
                vim.command('hide edit %s' % (relpath(product),))
            else:
                _cant_find(current, to_test=False, create=create)
        else:
            _cant_find(current, to_test=True, create=create)


def run_python_tests(external):
    '''
    If the current file has unit tests, run them. If the current file is a
    unit test, run it. Running is asynchronous. Output is read into quickfix.
    '''
    if vim.current.buffer.name is None:
        print 'Not a file'
        return

    vim.command('silent wall')

    def get_test(filename):
        '''
        Try to find a test for the given file, regardless of whether it already
        looks like a test or not (some test-util modules look like tests, but
        aren't.) If not found, and the given file does look like a test, then
        relent and simply return the given file. Otherwise, we have failed to
        find the given file's tests, so return None.
        '''
        test = _find_test(filename)
        if test:
            return test
        else:
            if _looks_like_test(filename):
                return (filename)

    test = relpath(get_test(vim.current.buffer.name))
    if test:
        module = _filename_to_module(test)
        _run_unittest(module, external)
    else:
        print "Can't find test file"


# regular expressions used to detect test method and test class names

test_method_re = re.compile('''
    [ ]*        # optional preceding whitespace
    def         # the def keyword
    \ (test\w+) # a space then the (captured) test name
    \(          # open paren marks the end of the test name
''', re.VERBOSE)

test_class_re = re.compile('''
    [ ]*            # optional preceding whitespace
    class           # the class keyword
    \ (             # start capture of class name
      [tT]est\w+ |  # match classes named 'testX'
      \w+[tT]est    # or classes named 'Xtest'
    )
    \(              # open paren marks the end of the class name
''', re.VERBOSE)

def run_single_test_method(external):
    '''
    Runs the single test method currently under the text cursor
    '''
    if vim.current.buffer.name is None:
        print 'Not a file'
        return

    current_file = relpath(vim.current.buffer.name)
    current_line_no = vim.current.window.cursor[0] - 1

    vim.command('silent wall')

    # find the names of the test method and the test class under the cursor
    line, method = _find_prior_matching_line(current_line_no, test_method_re)
    if method is None:
        print "Can't find test method"
        return
    _, klass = _find_prior_matching_line(line, test_class_re)
    if klass is None:
        print "Can't find test class"
        return

    # create command of the form
    # python -m unittest --verbose package1.package2.module.class.method 
    module = _filename_to_module(current_file)
    dotted_method_name = '%s.%s.%s' % (module, klass, method)
    _run_unittest(dotted_method_name, external, verbose=True)



# -- private ----

def _normalise(path):
    return path.rstrip(r'/')


class _DirnameConvention(object):
    '''
    Each instance represents one possible convention for name of unittest
    subdirectories.
    '''
    def __init__(self, testdir):
        self.testdir = testdir

    def __repr__(self):
        return '<DirnameConvention %s>' % (self.testdir,)

    def is_test(self, path):
        '''
        is the given path a possible test directory?
        '''
        last_path_cmpt = split(_normalise(path))[1].lower()
        return last_path_cmpt == self.testdir.lower()

    def is_product(self, path):
        '''
        Is the given path a possible product directory? (ie. not a test dir)
        This function only exists because in subclasses, it is not simply
        defined as 'not is_test'.
        '''
        return not self.is_test(path)

    def to_product(self, path):
        '''
        If the given path is a test directory, convert it to the corresponding
        product directory
        '''
        path = _normalise(path)
        if self.is_test(path):
            return split(path)[0]
        else:
            raise RuntimeError('not a test path: ' + path)

    def to_test(self, path):
        '''
        If the given path is a product directory, convert it to the
        corresponding test directory
        '''
        path = _normalise(path)
        if not self.is_test(path):
            return relpath(join(path, self.testdir))
        else:
            raise RuntimeError('not a product path: ' + path)


class _DirnameInTheSameDir(_DirnameConvention):
    '''
    Special case for when tests are stored in same dir as product code
    '''
    def __init__(self):
        self.testdir = '.'
    def is_test(self, _):
        return True
    def is_product(self, _):
        return True
    def to_product(self, path):
        return path
    def to_test(self, path):
        return path

# enumerate all known test subdir naming conventions
_dir_conventions = map(_DirnameConvention, test_subdir_names)
_dir_conventions.append(_DirnameInTheSameDir())


class _FilenameConvention(object):
    '''
    Each instance represents one possible convention for converting between
    product and test file names.

    Construct with a template param which indicates the style by which names of
    unit test files might be derived from the names of product files. eg:
    _FilenameConvertion('test-*') represents the convention that file
    'hello.py' is tested by 'test-hello.py'.
    '''
    def __init__(self, template):
        self.template = template
        self.regex = re.compile(
            self.template.replace('*', '(.+)') + '$',
            flags=re.IGNORECASE,
        )

    def __repr__(self):
        return '<FilenameConvention %s>' % (self.template,)

    def is_test(self, filename):
        '''
        is the given filename a possible test file?
        '''
        return fnmatch(filename, self.template) # is case insensitive

    def to_product(self, filename):
        '''
        convert given name of test to name of corresponding product file
        '''
        if self.is_test(filename):
            match = self.regex.match(filename)
            return match.group(1)
        else:
            raise RuntimeError('not a test filename: ' + filename)

    def to_test(self, filename):
        '''
        convert the given name of product code to corresponding test module
        '''
        if not self.is_test(filename):
            return self.template.replace('*', filename)
        else:
            raise RuntimeError('not a product filename: ' + filename)

# enumerate all known test file naming conventions
_file_conventions = map(_FilenameConvention, test_filenames)



def _filename_to_module(filename):
    pathname = splitext( splitdrive(filename)[1] )[0]
    return pathname.replace(sep, '.')


def _run_unittest(test, external, verbose=False):
    # create command of the form
    #   python -m unittest package.package.module
    # and run asynchronously
    verbose_flag = '--verbose ' if verbose else ''
    command = 'python -m unittest %s%s' % (verbose_flag, test,)
    print command
    vim.command("silent compiler pyunit")
    vim.command("silent call RunCommand('%s', %d)" % (command, external))


def _find_prior_matching_line(line_number, pattern):
    '''
    Starting at given line number and working upwards towards start of file,
    look for first line which matches the given regex pattern. Return line
    number and match group 1. (e.g. method name or class name extracted from
    a matching line defining a method or class)
    '''
    testName = None
    while line_number >= 0:
        line = vim.current.buffer[line_number]
        if pattern.match(line):
            testName = pattern.match(line).groups(1)[0]
            break
        line_number -= 1
    return line_number, testName


def _edit_new_file(path, name, ext):
    '''
    create new file for opening in vim
    '''
    # create directory if doesn't exist
    if not isdir(path):
        os.mkdir(path)

    # make this new dir a Python package if not already
    init = join(path, '__init__.py')
    if not os.path.isfile(init):
        open(init, 'a').close()

    # edit the new file
    vim.command('edit ' + join(path, name + ext))


def _cant_find(orig, to_test, create):
    '''
    Can't find test or product to toggle to from file 'orig'.
    Either display a message, or else just create it.
    '''
    path, name, ext = _get_filename_components(orig)
    if create:
        dirname_convention = _dir_conventions[preferred_subdir]
        filename_convention = _file_conventions[preferred_filename]
        if to_test:
            path = dirname_convention.to_test(path)
            name = filename_convention.to_test(name)
        else:
            path = dirname_convention.to_product(path)
            name = filename_convention.to_product(name)
        _edit_new_file(path, name, ext)
    else:
        filetype = "test" if to_test else "product"
        print "Can't find " + filetype


def _get_filename_components(fullname):
    '''
    Convert 'C:\dir1\dir2\myfile.exe' to ('C:\dir1\dir2', 'myfile', '.ext')
    '''
    path = dirname(fullname)
    name, ext = splitext(basename(fullname))
    return path, name, ext


def _looks_like_test(filename):
    '''
    return true if the given filename looks like it could be a unit test.
    Does not actually check the filesystem to verify whether it *has*
    some tests.
    '''
    _, name, __ = _get_filename_components(filename)
    return any(
        fileconv.is_test(name)
        for fileconv in _file_conventions
    )


def _find_test(filename):
    '''
    Convert the given product code filename into the corresponding test file
    name, by searching for the first file that exists amongst all known test
    naming conventions.
    '''
    path, name, ext = _get_filename_components(filename)
    for dirconv in _dir_conventions:
        if dirconv.is_product(path):
            testdir = dirconv.to_test(path)

            for fileconv in _file_conventions:
                if not fileconv.is_test(name):
                    testfile = fileconv.to_test(name)

                    test = join(testdir, testfile + ext)
                    if os.path.isfile(test):
                        return test


def _find_product(filename):
    '''
    Convert the given test filename into corresponding product code file name,
    by searching for the first file that exists amongst all the possible
    product filenames. List of all possible product filenames is obtained by
    applying the reverse of all known test naming conventions to the given
    filename.
    '''
    path, name, ext = _get_filename_components(filename)
    for dirconv in _dir_conventions:
        if dirconv.is_test(path):
            proddir = dirconv.to_product(path)

            for fileconv in _file_conventions:
                if fileconv.is_test(name):
                    prodfile = fileconv.to_product(name)

                    product = join(proddir, prodfile + ext)
                    if os.path.isfile(product):
                        return product

