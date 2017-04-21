# vision
vision software for USNA_SUAS
This package requires auvsi's interop module
(documentation here: http://auvsi-suas-competition-interoperability-system.readthedocs.io/en/latest/)
to get / build interop:
Prerequisites:
Git
Python
Virtualenv
Pip

1.)Command: git clone https://github.com/auvsi-suas/interop
2.)Command: cd \interop\interop\client
3.)Command: python setup.py install

*note: build will sometimes fail if you lack the requisite python packages to run the system,
most common is futures, to fix this:
Command: pip install futures
*as a general python rule, if a build or run fails on windows, do the following:
check that
