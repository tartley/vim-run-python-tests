
help:
	# this makefile is only intended to help me out during development of
	# run_python_tests. It is unlikely to be of any use to anyone else.
	# for the record, though, I generally run it from a Windows XP Cmd
	# shell with Cygwin binaries foremost on the PATH

install:
	cp -r ftplugin ~/.vim
	cp README.txt ~/.vim/ftplugin/python/run_python_tests

zip:
	rm -rf dist
	mkdir dist
	cp -r ftplugin dist
	cp README.txt dist/ftplugin/python/run_python_tests
	(cd dist; zip -r run_python_tests.zip ftplugin)

