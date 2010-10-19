Run Python Tests

    Vim scripts to run Python unit tests.

    Docs and download:
        http://www.vim.org/scripts/script.php?script_id=3281

    Development Hg repository:
        http://bitbucket.org/tartley/vim_run_python_tests

    Only currently tested on Windows XP, gVim.exe 7.2 & 7.3.
    Does not work on vim.exe, unless you recompile to include Python support.


DESCRIPTION
    
    Provides key bindings to:

    <Leader>a : toggles between the Python file in the current buffer and its
                unit tests.
    F4 : Toggle the quickfix window open or closed.
    F5 : Run the Python file in the current buffer.
         (i.e. run "python dir\subdir\file.py".)
    F6 : Find & run the unit tests of the Python file in the current buffer.
         (i.e. find the unittest module as described below, then run
         "python -m unittest package.subpackage.module")
    F7 : Run the single test method under the cursor
         (i.e. find the name of the test method the cursor is in, find its
         test class name, then run
         "python -m unittest --verbose package.subpack.module.class.method")

    For F5, F6, & F7, you will want to check what Vim's current directory is.
    This will affect the path or sequence of packages used to reference your
    test module. Set the current directory in Vim using the :cd command. It
    should be set to the same directory that you'd have to be in to execute
    your tests from the command-line, which is generally your project root.

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
                 |-a bunch of files in here, including:
                 |-README.txt


TROUBLESHOOTING

    Q) When I try to run tests, I see a traceback from unittest, such as:
    "ImportError: No module named X", or "ValueError: Attempted relative
    import beyond toplevel package"

    A) Are you sure Vim's current working directory is correct? These are the
    errors you will likely see if it is not. Can you run your module's unit
    tests from the command line from the same directory that Vim is currently
    in?
    

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
    * Allow user to configure the commands used to run tests.
    * Instead of printing out status messages, can we prepend them to the
      output in the quickfix window?


THANKS

    Pretty much all of this is stolen from various existing scripts at 
    vim.org, or from my awesome colleagues at Resolver Systems.


CONTACT

    I know nothing about Vim scripting, so I'd love to hear about it if you
    have problems with this script, or ideas on how it could be better.

    Jonathan Hartley, tartley@tartley.com

