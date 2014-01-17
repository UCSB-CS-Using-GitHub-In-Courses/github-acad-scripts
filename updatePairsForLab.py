#!/usr/bin/python

# This script looks up every pair team that exists.
# It then,for each pair team
#  (4) creates a repo for the team (if it doesn't already exist)
#  (5) populates it, but only if it was JUST created.

import getpass
import argparse
import os
import sys

from github_acadwf import addPyGithubToPath
from github_acadwf import updatePairsForLab
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


GHA_WORKDIR = getenvOrDie('GHA_WORKDIR',
                          "Error: please set GHA_WORKDIR to a writeable scratch directory")

GHA_STARTPOINT_DIR = getenvOrDie('GHA_STARTPOINT_DIR',
                          "Error: please set GHA_STARTPOINT_DIR to a readable directory")



# Now try to get the Google Spreadsheet Data

parser = argparse.ArgumentParser(description='Update lab for pairs')

parser.add_argument('lab',metavar='labxx',  
                    help="which lab (e.g. lab00, lab01, etc.)")

parser.add_argument('-u','--githubUsername', 
                    help="github username, default is current OS user",
                    default=getpass.getuser())

parser.add_argument('-t','--teamPrefix', 
                    help="prefix of teams to create",
                    default="")


args = parser.parse_args()



if not os.access(GHA_WORKDIR, os.W_OK):
    print(GHA_WORKDIR + " is not a writable directory.")
    sys.exit(1)



pw = getpass.getpass()
g = Github(args.githubUsername, pw, user_agent="PyGithub")

org= g.get_organization(GHA_GITHUB_ORG)


updatePairsForLab(g,org,args.lab,GHA_WORKDIR, GHA_STARTPOINT_DIR, args.teamPrefix)







