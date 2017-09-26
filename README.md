# runco

[![Updates](https://pyup.io/repos/github/kwierman/runco/shield.svg)](https://pyup.io/repos/github/kwierman/runco/)
[![Python 3](https://pyup.io/repos/github/kwierman/runco/python-3-shield.svg)](https://pyup.io/repos/github/kwierman/runco/)
[![Build Status](https://travis-ci.org/kwierman/runco.svg?branch=master)](https://travis-ci.org/kwierman/runco)
[![Documentation Status](https://readthedocs.org/projects/runco/badge/?version=latest)](https://runco.readthedocs.io/en/latest/?badge=latest)
[![pypi](https://img.shields.io/pypi/v/runco.svg)](https://pypi.python.org/pypi/runco)

Some tools for RunCos to access data faster and with vigor.

* Open Source License: MIT license
* Documentation: https://runco.readthedocs.io.

## Installation

This package is typically installed in a python virtual environment. Instructions can be found [here](https://virtualenvwrapper.readthedocs.io/en/latest/).

Once you have `virtualenv` and/or `virtualenvwrapper` installed, you can make an environment for the runco tools to sit:

``` bash
➜  Desktop mkvirtualenv runco
New python executable in /Users/wier702/.virtualenvs/runco/bin/python
Installing setuptools, pip, wheel...done.
virtualenvwrapper.user_scripts creating /Users/wier702/.virtualenvs/runco/bin/predeactivate
virtualenvwrapper.user_scripts creating /Users/wier702/.virtualenvs/runco/bin/postdeactivate
virtualenvwrapper.user_scripts creating /Users/wier702/.virtualenvs/runco/bin/preactivate
virtualenvwrapper.user_scripts creating /Users/wier702/.virtualenvs/runco/bin/postactivate
virtualenvwrapper.user_scripts creating /Users/wier702/.virtualenvs/runco/bin/get_env_details
(runco) ➜  Desktop
```

Then, `git clone` the tools into a handy directory (which you can then `cd` into).

``` bash
(runco) ➜  Desktop git clone https://github.com/kwierman/runco
Cloning into 'runco'...
remote: Counting objects: 111, done.
remote: Total 111 (delta 0), reused 0 (delta 0), pack-reused 111
Receiving objects: 100% (111/111), 4.84 MiB | 380.00 KiB/s, done.
Resolving deltas: 100% (40/40), done.
(runco) ➜  Desktop cd runco
(runco) ➜  runco git:(master)
```

The installation step is performed by typing in the command:

``` bash
(runco) ➜  runco git:(master) python setup.py install
```

This should pull all the dependencies and install them locally before installing the main package.

> Warning: Kevin is about to unpin the dependency tree, so this may create depenency issues at compile time. Sorry, but the dependencies were out of date.

The last important step is to create a config file for the runco tools. Ask [Kevin](mailto:kwierman@gmail.com) how to do this. This would be included in the documentation, but need to live in private documentation only.


## Running the notebooks

After installing the base packages, you can `cd` into the notebooks directory and run `jupyter`.

``` bash
cd <wherever you installed runco>/runco/notebook
jupyter-notebook
```
