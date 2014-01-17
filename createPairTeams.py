#!/usr/bin/python

# This script reads all the users and pairs from the CSV files created
# by the Google Form.

# It first runs all the checks on the CSV file for names, finding duplicates,
# and disambiguating by adding _A _B, etc.

# It then,for each line in the pair spreadsheet
#  (1) creates the Pair_FirstName_SecondName team
#  (2) adds the github users for both student to that team

import getpass
import argparse
import os
import sys

from github_acadwf import addPyGithubToPath
from github_acadwf import addTeamsForPairsInFile
from github_acadwf import getenvOrDie
from github_acadwf import getCSVFromURL

addPyGithubToPath()

from github import Github
from github import GithubException
                  

GHA_GITHUB_ORG = getenvOrDie("GHA_GITHUB_ORG",
                        "Error: please set GHA_GITHUB_ORG to name of github organization for the course, e.g. UCSB-CS56-W14")


GHA_STUDENT_LIST_URL = getenvOrDie('GHA_STUDENT_LIST_URL',
                                   "Error: please set GHA_STUDENT_LIST_URL to url of Google Spreadsheet with the github ids")

GHA_PAIR_LIST_URL = getenvOrDie('GHA_PAIR_LIST_URL',
                                   "Error: please set GHA_PAIR_LIST_URL to url of Google Spreadsheet with the github ids")

GHA_WORKDIR = getenvOrDie('GHA_WORKDIR',
                          "Error: please set GHA_WORKDIR to a writeable scratch directory")


GHA_STARTPOINT_DIR = getenvOrDie('GHA_STARTPOINT_DIR',
                          "Error: please set GHA_STARTPOINT_DIR to a readable directory")


parser = argparse.ArgumentParser(description='Setup teams for pairs')

parser.add_argument('-u','--githubUsername', 
                    help="github username, default is current OS user",
                    default=getpass.getuser())

args = parser.parse_args()


if not os.access(GHA_WORKDIR, os.W_OK):
    print(GHA_WORKDIR + " is not a writable directory.")
    sys.exit(1)


csvFile  = getCSVFromURL(GHA_STUDENT_LIST_URL,GHA_WORKDIR,"students.csv",
              " check value of GHA_STUDENT_LIST_URL environment variables")

pairFile  = getCSVFromURL(GHA_PAIR_LIST_URL,GHA_WORKDIR,"pairs.csv",
              " check value of GHA_PAIR_LIST_URL environment variables")



pw = getpass.getpass()
g = Github(args.githubUsername, pw, user_agent="PyGithub")

org= g.get_organization(GHA_GITHUB_ORG)


addTeamsForPairsInFile(g,org,csvFile,pairFile)








