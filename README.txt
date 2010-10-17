Vim Run Python Tests

    http://bitbucket.org/tartley/vim_run_python_tests

    Vim scripts to run Python unit tests.

    Only currently tested on Vim 7.2 on Windows XP.
    

DESCRIPTION
    
    Provides key bindings to:

    <Leader>a : toggles between the Python file in the current buffer and its
                unit tests.
    F4 : Toggle the quickfix window open or closed.
    F5 : Run the Python file in the current buffer
    F6 : Find & run the unit tests of the Python file in the current buffer
    F7 : Run the single test method under the cursor

    All running of files or tests is done asynchronously, so you can continue
    using Vim while it runs. When complete, the output is read into Vim's
    quickfix window.
    
    Alternatively, pressing Shift-F5, -F6, or -F7 will run the respective
    command in a new text terminal, which will remain open to display the
    results, and will automatically re-run the command whenever it detects
    changes to any file in or below the current directory.

    When looking for the test module that corresponds to the current file,
    we search in the same dir, and in a bunch of likely-named subdirectories
    (e.g. 'test', 'tests', 'unittest', 'unittests') for a file of an
    likely-sounding test name. e.g. when 'widget.py' is the current buffer,
    we search for 'testwidget.py', 'test_widget.py', 'widget_tests.py', etc.


INSTALL

    Unzip into your ~/.vim folder. It should provide:

    ~/.vim
        |-ftplugin
           |-python
              |-run_python_tests.vim
              |-run_python_tests
                 |-run_python_tests.py
                 |-test_run_python_tests.py
                 |-README.txt


TROUBLESHOOTING

    Q) When I try to run tests, I see a traceback from unittest, such as:
    "ImportError: No module named X", or "ValueError: Attempted relative
    import beyond toplevel package"

    A) Are you sure Vim's current working directory is correct? Set it using
    the Vim :cd command. I have to set it to my project root directory for me
    to be able to run my unittests. This is true if I'm trying to run the
    tests from the command-line too.


PYTHON TRACEBACKS IN THE VIM QUICKFIX WINDOW

    The default value of Vim's errorformat variable for working with Python
    only shows one entry from each traceback, which seems unhelpful to me. To
    fix this, you can create a file ~/.vim/compiler/pyunit, which contains
    just:

        CompilerSet efm=\%A\ \ File\ \"%f\"\\,\ line\ %l\\,\ %m,%C\ %m,%Z

    Now when you run the ':compiler pyunit' command (as run_python_tests
    does whenever you press F5, F6, or F7), Vim's quickfix window will display
    all the entries in each traceback.


TODO

    * Make it all work on Linux
    * Instead of printing out status messages, can we prepend them to the
      output in the quickfix window?


THANKS

    Pretty much all of this is stolen from various existing scripts at 
    vim.org, or from my awesome colleagues at Resolver Systems.


CONTACT

    I know nothing about Vim scripting, so I'd love to hear about it if you
    have problems with this script, or ideas on how it could be better.

    Jonathan Hartley, tartley@tartley.com

