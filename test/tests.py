'''
Created on 14.05.2015

@author: Philip Schoemig
'''

import os
import pytest
import sys


if __name__ == "__main__":
    testdir = os.path.dirname(os.path.abspath(__file__))
    srcdir = os.path.abspath(os.path.join(testdir, '..', 'src'))

    # Append source directory to search path
    sys.path.append(srcdir)

    # Setup pytest arguments
    args = ['--cov', srcdir]
    if '--pep8' in sys.argv:
        args.append('--pep8')
        args.append(srcdir)

    # Execute pytest on the test directory
    args.append(testdir)
    sys.exit(pytest.main(args))
