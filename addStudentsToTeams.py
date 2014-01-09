#!/usr/bin/python

# This script reads all the users from the CSV file created
# by the Google Form.

# If first checks for any duplicate first names.  If there are duplicate
# first names, it deambiguates the first names by adding first letters of
# the last name until the names are distinguished.

# It then:
#  (1) checks if the github user exists (bails, if not)
#  (2) creates the Student_FirstName team (if not already there)
#  (3) adds the github user to the Student_FirstName team and AllStudents team

from __future__ import print_function

import getpass
import sys
import argparse
import csv

from github_acadwf import addPyGithubToPath
from github_acadwf import addStudentsFromFileToTeams
from github_acadwf import getAllStudentsTeam
from github_acadwf import createTeam
from github_acadwf import getenvOrDie
from github_acadwf import getCSVFromURL

addPyGithubToPath()

from github import Github
from github import GithubException

import os
import sys

GHA_GITHUB_ORG = getenvOrDie("GHA_GITHUB_ORG",
                        "Error: please set GHA_GITHUB_ORG to name of github organization for the course, e.g. UCSB-CS56-W14")


GHA_STUDENT_LIST_URL = getenvOrDie('GHA_STUDENT_LIST_URL',
                                   "Error: please set GHA_STUDENT_LIST_URL to url of Google Spreadsheet with the github ids")

GHA_WORKDIR = getenvOrDie('GHA_WORKDIR',
                          "Error: please set GHA_WORKDIR to a writeable scratch directory")


# Now try to get the Google Spreadsheet Data

csvFile  = getCSVFromURL(GHA_STUDENT_LIST_URL,GHA_WORKDIR,"students.csv",
              " check value of GHA_WORKDIR")

                   


parser = argparse.ArgumentParser(description='add students to teams')

parser.add_argument('-u','--githubUsername', 
                    help="github username, default is current OS user",
                    default=getpass.getuser())

args = parser.parse_args()
pw = getpass.getpass()

g = Github(args.githubUsername, pw, user_agent="PyGithub")
org= g.get_organization(GHA_GITHUB_ORG)

allStudentsTeam = getAllStudentsTeam(org)

if (allStudentsTeam == False):
    print("creating AllStudents Team")
    team = createTeam(org, "AllStudents")
    allStudentsTeam = getAllStudentsTeam(org,refresh=True)
else:
    print("AllStudents team found")

addStudentsFromFileToTeams(g,org,csvFile)








