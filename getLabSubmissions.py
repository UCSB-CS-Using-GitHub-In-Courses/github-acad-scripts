#!/usr/bin/python

import os

from github_acadwf import getenvOrDie
from github_acadwf import getCSVFromURL


GHA_GITHUB_ORG = getenvOrDie("GHA_GITHUB_ORG",
                        "Error: please set GHA_GITHUB_ORG to name of github organization for the course, e.g. UCSB-CS56-W14")


GHA_STUDENT_LIST_URL = getenvOrDie('GHA_STUDENT_LIST_URL',
                                   "Error: please set GHA_STUDENT_LIST_URL to url of Google Spreadsheet with the github ids")

GHA_STAFF_LIST_URL = getenvOrDie('GHA_STAFF_LIST_URL',
                                   "Error: please set GHA_STAFF_LIST_URL to url of Google Spreadsheet with the github ids")

GHA_WORKDIR = getenvOrDie('GHA_WORKDIR',
                          "Error: please set GHA_WORKDIR to a writeable scratch directory")


GHA_STARTPOINT_DIR = getenvOrDie('GHA_STARTPOINT_DIR',
                          "Error: please set GHA_STARTPOINT_DIR to a readable directory")



labSubmissionsDir = GHA_WORKDIR + "/labSubmissions"
if not os.access(labSubmissionsDir, os.W_OK):
  os.mkdir(labSubmissionsDir, 0700)

import getpass
import sys
import argparse
from github_acadwf import pullRepoForGrading

# In the main directory of the repo where you are developing with PyGithub,
# type:
#    git submodule add git://github.com/jacquev6/PyGithub.git PyGithub
#    git submodule init
#    git submodule update
#
# That will populate a PyGithub subdirectory with a clone of PyGithub
# Then, to add it to your Python path, you can do:

sys.path.append("./PyGithub");

from github import Github
from github import GithubException

parser = argparse.ArgumentParser(description='Pull repos for grading that start with a certain prefix')
parser.add_argument('prefix',help='prefix e.g. lab00')
parser.add_argument('-u','--githubUsername',
                    help="github username, default is current OS user",
                    default=getpass.getuser())

args = parser.parse_args()

username = args.githubUsername
pw = getpass.getpass()
g = Github(username, pw, user_agent='PyGithub')

org = g.get_organization(GHA_GITHUB_ORG)

## TODO: Add some error checking code here to see whether
##  the lookup was successful.  Do we try/except or check the return value?

repos = org.get_repos()

for repo in repos:
  if repo.name.startswith(args.prefix):
    print(repo.name)
    pullRepoForGrading(repo,labSubmissionsDir+'/'+args.prefix)
