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

addPyGithubToPath()

from github import Github
from github import GithubException

import os
import sys

GHA_GITHUB_ORG = os.environ.get('GHA_GITHUB_ORG')

if GHA_GITHUB_ORG==None:
   print("Error: please set GHA_GITHUB_ORG to name of github organization for the course, e.g. UCSB-CS56-W14")
   sys.exit()

GHA_STUDENT_LIST_URL = os.environ.get('GHA_STUDENT_LIST_URL')

if GHA_STUDENT_LIST_URL==None:
   print("Error: please set GHA_STUDENT_LIST_URL to url of Google Spreadsheet with the github ids")
   sys.exit()

GHA_WORKDIR = os.environ.get('GHA_WORKDIR')

if GHA_WORKDIR==None:
   print("Error: please set GHA_WORKDIR to a writeable scratch directory")
   sys.exit()

if not os.access(GHA_WORKDIR, os.W_OK):
   print("GHA_WORKDIR is set to " + GHA_WORKDIR+ " which is not a writeable scratch directory; please fix this and try again.")
   sys.exit()

# Now try to get the Google Spreadsheet Data

sys.path.append("requests");

import requests
response = requests.get(GHA_STUDENT_LIST_URL + '&output=csv')
assert response.status_code == 200, 'Wrong status code'

csvFile = GHA_WORKDIR + "/students.csv"

with open(csvFile, 'w') as f:
    print (response.content,file=f)

print("retrieved CSV file from URL")
                      
defaultInputFilename =  csvFile

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








