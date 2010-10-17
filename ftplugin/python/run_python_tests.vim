" run_python_tests.vim
" v0.1 17 Oct 2010
" See README in ftplugin/python/run_python_tests

" Make sure we run only once
if exists("loaded_run_python_tests")
    finish
endif
let loaded_run_python_tests = 1

" The dir in which this script's dependencies live
let s:rootdir = fnamemodify(expand("<sfile>"), ":h")."\\run_python_tests\\"

" load python utility functions
" The 'execute' and 'fn*' functions make this more robust under various
" environments than simply using 'pyfile <filename>' would be.
execute "pyfile ".fnameescape(s:rootdir."run_python_tests.py")


"-------------------------------------------------------------------------
" toggle quickfix window open / closed

let s:quickfix_open = 0

function s:ToggleQuickfix()
    if s:quickfix_open == 0
        botright copen 15
        let s:quickfix_open = 1
    else
        cclose
        let s:quickfix_open = 0
    endif
endfunction

nnoremap <silent> <f4> :call <SID>ToggleQuickfix()<cr>


"-------------------------------------------------------------------------
" Toggle between a file and its unit test
" The second binding creates the test (or product) file if it doesn't exist.
nnoremap <silent> <Leader>a :python toggle_test()<cr>
nnoremap <silent> <Leader>A :python toggle_test(create=True)<cr>


"-------------------------------------------------------------------------
" Asynchronously run the given command 'internally', i.e. capturing output in
" the Vim quickfix window when done

" read the given file into the quickfix window
function! ReadFileIntoQuickfix(temp_file_name)
    " popualate quickfix withgout interrupting user
    exec 'cgetfile '.a:temp_file_name
    call delete(a:temp_file_name)

    " open the quickfix window
    botright copen 15
    let s:quickfix_open = 1

    " don't interrupt whatever user was doing
    wincmd p
    
    " clear the command area
    echo
    redraw 
endfunction


function RunCommandInternal(command)
    " clear the quickfix
    cgete ""

    let temp_file = tempname()

    execute 'silent !start /min cmd /C "'.a:command.' 2>&1 '.
        \ '| python "'.s:rootdir.'filtercwd.py" >'.temp_file
        \ '& vim --servername '.v:servername.' --remote-expr "ReadFileIntoQuickfix('."'".temp_file."')\""'"'
endfunction


"-------------------------------------------------------------------------
" Asynchronously run the given command 'externally', i.e. in an external
" cmd window, using 'rerun' (http://bitbucket.org/tartley/rerun)

function! RunCommandExternal(command)
    let command = 'python "'.s:rootdir.'rerun.py" '.a:command
    execute 'silent !start cmd /C '.command.''
endfunction


"-------------------------------------------------------------------------
" Asynchronously run the given command, and uses thereof

" run the given command
function! RunCommand(command, external)
    echo a:command
    if a:external == 1
        call RunCommandExternal(a:command)
    else
        call RunCommandInternal(a:command)
    endif
endfunction

" run the given python file
function! RunPythonFile(filename, external)
    let s:command = 'python '.expand(a:filename)
    compiler pyunit
    call RunCommand(s:command, a:external)
endfunction

" run the current buffer's Python file
function! RunCurrentPythonFile(external)
    silent wall
    call RunPythonFile("%", a:external)
endfunction

nnoremap <silent> <f5> :call RunCurrentPythonFile(0)<cr>
nnoremap <silent> <s-f5> :call RunCurrentPythonFile(1)<cr>

"-------------------------------------------------------------------------
" Run the unittests of the file in the current buffer
nnoremap <silent> <f6> :python run_python_tests(external=0)<cr>
nnoremap <silent> <s-f6> :python run_python_tests(external=1)<cr>

"-------------------------------------------------------------------------
" Run the single test method under the text cursor
nnoremap <silent> <f7> :python run_single_test_method(external=0)<cr>
nnoremap <silent> <s-f7> :python run_single_test_method(external=1)<cr>

