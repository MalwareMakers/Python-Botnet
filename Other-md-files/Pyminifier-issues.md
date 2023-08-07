# Pyminifier Issues

Unfortunately sometimes you might run into issues when trying to install pyminifier. Here are some places i would remcommened checking out if you come across any problems. 

## No 2to3 package: 
This is an error that occured to me completely at random after trying to re-install pyminifier: 

This is what the Error Looks like: 
-  `Collecting pyminifier
    Using cached pyminifier-2.1.tar.gz (47 kB)
    Preparing metadata (setup.py) ... error
    error: subprocess-exited-with-error

    × python setup.py egg_info did not run successfully.
    │ exit code: 1
    ╰─> [3 lines of output]
        Python 3.X support requires the 2to3 tool.
        It normally comes with Python 3.X but (apparenty) not on your distribution.
        Please find out what package you need to get 2to3and install it.
        [end of output]

    note: This error originates from a subprocess, and is likely not a problem with pip.
    error: metadata-generation-failed

    × Encountered error while generating package metadata.
    ╰─> See above for output.`

The solution can be found [here](https://stackoverflow.com/questions/75913887/this-thing-im-doing-wants-python-2to3-i-already-have-that-what-do-i-do)

1. First: `pip3 install --upgrade pip setuptools==57.5.0`
2. Then try installing pyminifier again: `pip3 install pyminifier`

## Some other Random issues: 

Im just going to link you to the pyminifier issues page on GitHub as I dont think I can cover every possible issue with pyminifier, so check [here](https://github.com/liftoff/pyminifier/issues) to try and solve some other issues. 