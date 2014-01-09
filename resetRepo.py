#!/usr/bin/python

# This script reads all the users from the CSV file created
# by the Google Form.

# If first checks for any duplicate first names.  If there are duplicate
# first names, it deambiguates the first names by adding first letters of
# the last name until the names are distinguished.

# It then,for each student
#  (1) creates the Student_FirstName team (if not already there)
#  (2) adds the github user id to that team
#  (3) adds the github user it to the AllStudents team
#  (4) creates a repo for the student (if it doesn't already exist)
#  (5) populates it, but only if it was JUST created.

import getpass
import argparse
import os
import sys

from github_acadwf import addPyGithubToPath
from github_acadwf import resetRepo
from github_acadwf import getenvOrDie
from github_acadwf import getCSVFromURL


addPyGithubToPath()

from github import Github
from github import GithubException
                      
import getpass

import sys

import argparse


from github_acadwf import makeUserDict
from github_acadwf import getUserList

sys.path.append("./PyGithub");

from github import Github
from github import GithubException



GHA_GITHUB_ORG = getenvOrDie("GHA_GITHUB_ORG",
                        "Error: please set GHA_GITHUB_ORG to name of github organization for the course, e.g. UCSB-CS56-W14")


GHA_STUDENT_LIST_URL = getenvOrDie('GHA_STUDENT_LIST_URL',
                                   "Error: please set GHA_STUDENT_LIST_URL to url of Google Spreadsheet with the github ids")

GHA_WORKDIR = getenvOrDie('GHA_WORKDIR',
                          "Error: please set GHA_WORKDIR to a writeable scratch directory")


GHA_STARTPOINT_DIR = getenvOrDie('GHA_STARTPOINT_DIR',
                          "Error: please set GHA_STARTPOINT_DIR to a readable directory")



# Now try to get the Google Spreadsheet Data

csvFile  = getCSVFromURL(GHA_STUDENT_LIST_URL,GHA_WORKDIR,"students.csv",
              " check value of GHA_WORKDIR")

parser = argparse.ArgumentParser(description='Update for lab only for new users')

parser.add_argument('lab',metavar='labxx',  
                    help="which lab (e.g. lab00, lab01, etc.)")

parser.add_argument('-u','--githubUsername', 
                    help="github username for admin user, default is current OS user",
                    default=getpass.getuser())

parser.add_argument('-g','--githubid',
                    help="reset repo ONLY for labxx_githubid",
                    default="")

args = parser.parse_args()

if not os.access(GHA_WORKDIR, os.W_OK):
    print(GHA_WORKDIR + " is not a writable directory.")
    sys.exit(1)

pw = getpass.getpass()
g = Github(args.githubUsername, pw, user_agent="PyGithub")

org= g.get_organization(GHA_GITHUB_ORG)

resetRepo(g,org,csvFile,args.lab,GHA_WORKDIR,GHA_STARTPOINT_DIR,args.githubid)







