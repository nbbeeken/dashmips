"""Run Publish Commands."""
import shutil
from shlex import split
from subprocess import run

shutil.rmtree('dist')
shutil.rmtree('build')
shutil.rmtree('dashmips.egg-info')

run(split('python setup.py sdist bdist_wheel'), shell=True)
run(split('twine upload dist/*'), shell=True)
