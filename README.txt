Vim run tests

    http://bitbucket.org/tartley/vim_run_tests

    Vim scripts to run the Python file in the current buffer, or to find and
    run its unit tests, or to run the single test method under the cursor.

    Only currently tested on Vim 7.2 on Windows XP. I'll be trying it on the
    latest Vim and on Ubuntu soon, and would love to hear your feedback on
    how it fares elsewhere.


DESCRIPTION

    A set of Vimscript and Python functions to:

    <Leader>a : toggles between the Python file in the current buffer and its
                unit tests.
    F4 : Toggle the quickfix window open or closed.
    F5 : Run the Python file in the current buffer
    F6 : Find & run the unit tests of the Python file in the current buffer
    F7 : Run the single test method under the cursor

    Running files or tests is done asynchronously in the background,
    and when complete, the output is read into Vim's quickfix window.

    Alternatively, pressing Shift-F5, -F6 or -F7 will run the respective
    command in a new text terminal, which will remain open to display the
    results, and will automatically re-run the command whenever it detects
    changes to any file in or below the current directory. This feature
    relies upon the rerun.py script being on the PATH:
    http://bitbucket.org/tartley/rerun


PYTHON TRACEBACKS IN THE VIM QUICKFIX WINDOW

    The default value of Vim's errorformat variable for working with Python
    only shows one entry from each traceback, which seems unhelpful to me. To
    fix this, create a file ~/.vim/compiler/pyunit, which contains just:

        CompilerSet efm=\%A\ \ File\ \"%f\"\\,\ line\ %l\\,\ %m,%C\ %m,%Z

    When you now run the ':compiler pyunit' command (as the run_tests script
    does whenever you press F5, F6, or F7), Vim's quickfix window will now
    display all entries from tracebacks.


INSTALL

    Unzip into your ~/.vim folder. It should provide:

    ~/.vim
        |-ftplugin
           |-python
              |-run_tests.vim
              |-run_tests
                 |-run_tests.py
                 |-test_run_tests.py
                 |-README.txt


TROUBLESHOOTING

Q) When I try to run tests, I see a traceback from unittest, such as:
    "ImportError: No module named X", or
    "ValueError: Attempted relative import beyond toplevel package"

A) Are you sure Vim's current working directory is correct? Set it using the
Vim :cd command. I have to set it to my project root directory for me to be
able to run my unittests. This is true if I'm trying to run the tests from the
command-line too.


THANKS

    Pretty much every idea in here came first from my awesome colleagues at
    Resolver Systems.


CONTACT

    I'd love to hear about it if you have problems with this script, or ideas
    on how it could be better.

    Jonathan Hartley, tartley@tartley.com

