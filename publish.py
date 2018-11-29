"""Run Publish Commands."""
import shutil
import sys
from shlex import split
from subprocess import run

shutil.rmtree('dist', ignore_errors=True)
shutil.rmtree('build', ignore_errors=True)
shutil.rmtree('dashmips.egg-info', ignore_errors=True)
shutil.rmtree('dashmips/__pycache__', ignore_errors=True)
shutil.rmtree('dashmips/syscalls/__pycache__', ignore_errors=True)
shutil.rmtree('dashmips/instructions/__pycache__', ignore_errors=True)
shutil.rmtree('dashmips/plugins/__pycache__', ignore_errors=True)
shutil.rmtree('.mypy_cache', ignore_errors=True)


if 'clean' in sys.argv:
    sys.exit(0)  # Exit before we do anything more

run(split('python setup.py sdist bdist_wheel'), shell=True)
run(split('twine upload dist/*'), shell=True)
