Run Python Tests

    Vim scripts to run Python unittest modules.

    Docs and download:
        http://www.vim.org/scripts/script.php?script_id=3281

    Development Hg repository:
        http://bitbucket.org/tartley/vim_run_python_tests

    Only currently tested on:
        gVim.exe 7.2, 7.3.
        Windows XP, Ubuntu 10.10.
    Does not work in vim.exe, which does not include Python support.


INSTALL

    Unzip into your home .vim or vimfiles folder. It should provide:

    ~/.vim
        |-ftplugin
           |-python
              |-run_python_tests.vim
              |-run_python_tests
                 |-a bunch of files in here, including:
                 |-README.txt


DESCRIPTION
    
    Provides key bindings to:

    <Leader>a : toggles between the Python file in the current buffer and its
                unit tests. ('<Leader>' is some Vim convention, which for me
                means ',' (comma.). So press 'comma' then 'a' (for alternate?)
                in succession.

    F4 : Toggle the quickfix window open or closed.

    F5 : Run the Python file in the current buffer.
         (e.g. run "python dir\subdir\file.py".)

    F6 : Find & run the unit tests of the Python file in the current buffer.
         (e.g. find the unittest module as described below, then run
         "python -m unittest package.subpackage.module")

    F7 : Run the single test method under the cursor
         (e.g. find the name of the test method the cursor is in, find its
         test class name, then run
         "python -m unittest --verbose package.subpack.module.class.method")

    All running of files or tests is done asynchronously, so you can continue
    using Vim while it runs. When complete, the output is read into Vim's
    quickfix window.
    
    Alternatively, pressing Shift-F5, Shift-F6, or Shift-F7 will run the
    respective command in a new text terminal, which will remain open to
    display the results, and will automatically re-run the command whenever it
    detects changes to any file in or below the current directory.


ASSUMPTIONS

    Run_python_tests makes some assumptions.

    For F5, F6 or F7 to work, you need to set things up so that the commands
    they generate (examples of which are shown above) will run. In particular:

    * Your tests need to be runnable by unittest
    * Vim needs to be in the correct working directory (set using :cd) for
      the commands as shown above to work. For my code, this is generally my
      project root directory. If I am in a higher or lower directory, then I
      get "ImportError: No module named X", or "ValueError: Attempted relative
      import beyond toplevel package."

    When looking for the test module that corresponds to the current file,
    we search in the same dir, and in a bunch of likely-named subdirectories
    (e.g. 'test', 'tests', 'unittest', 'unittests') We search these dirs
    for a file of a likely-sounding test name. e.g. when 'widget.py' is the
    current buffer, we search for testwidget.py, test_widget.py,
    widget_test.py, etc. For a complete and up-to-date list, see the source
    code run_python_tests.py.


PYTHON TRACEBACKS IN THE VIM QUICKFIX WINDOW

    The default value of Vim's errorformat variable for working with Python
    only shows one entry from each traceback, which seems unhelpful to me. To
    fix this, you can create a file in your home .vim or vimfiles folder,
    called compiler/pyunit, which just contains:

        CompilerSet efm=\%A\ \ File\ \"%f\"\\,\ line\ %l\\,\ %m,%C\ %m,%Z

    Now when you run the ':compiler pyunit' command (as run_python_tests
    does whenever you press F5, F6, or F7), Vim's quickfix window will display
    all the entries in each traceback.


TODO

    * Make it all work on Linux
    * Allow user to configure the commands used to run tests.
    * Allow user to configure the names of test directories and the format of
      test module names.
    * Instead of printing out status messages, can we prepend them to the
      output in the quickfix window?


THANKS

    Pretty much all of this is stolen from various existing scripts at 
    vim.org, or from my awesome colleagues at Resolver Systems.


CHANGES

    0.2, 21 Oct 2010
        Tested on Windows XP, Vim7.3.
        Tested on Ubuntu, Vim7.2.
    0.1, 17 Oct 2010
        Tested on Vim7.2, Windows XP.
        Works in gVim, but not in vim.exe, which doesn't support Python.

CONTACT

    I know nothing about Vim scripting, so I'd love to hear about it if
    this doesn't work for you, or if you can help to correct any of my
    egregious errors.

    Jonathan Hartley, tartley@tartley.com
