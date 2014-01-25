# Quick Reference for github-acad-scripts

Scripts for using github.com in Academic Courses

## Table of Contents
* [Getting Started](#getting-started)
* [Creating a new lab (preliminary for TA beta testing)](#to-create-a-new-lab-prelimninary-version-for-ta-beta-testing)
* [Creating a new lab (for all students, but NOT pairs)](#to-create-a-new-lab-real-version-for-all-students-but-not-pairs)
* [Creating a new lab for ONE student](#to-create-a-new-lab-for-one-specific-student)
* [Creating pair teams](#creating-pair-teams)
* [Creating repo for pair teams](#creating-repo-for-pair-teams)

## Getting started

Do the [one-time steps](#getting-started---one-time-steps) at the bottom of this document.

EACH TIME: 

1. cd into your github-acad-scripts directory

2. ```git pull`` to update any changes

3. run the script env.sh by typing 
 ```. env.sh```
 
## To create a new lab (prelimninary version for TA beta testing)

1. cd into CS56-W14-Labs

2. create a new subdirectory (e.g. lab03)

3. populate it, and then git add, git commit, git push.

4. cd into github-acad-scripts and do:

 ```./updateForLab.py --staff -u githubAdminUser labXX```
 
This will create the private repos ONLY for those github ids listed in the Google Doc referred to by GHA_STAFF_LIST_URL
 
If your current effective unix userid is the same as the githubAdminUser that you want to use, you can omit the githubAdminUser flag.
 
## To create a new lab (real version for all students, but not pairs):

This assumes the lab has already been created in CS56-W14-Labs

1. cd into CS56-W14-Labs

2. ```git pull```

3. cd into github-acad-scripts and do:

 ```./updateForLab.py -u githubAdminUser labXX ```
 
This will create the private repos for ALL github ids listed in the Google Doc referred to by GHA_STUDENT_LIST_URL
 
 
## To create a new lab for ONE specific student:

This assumes the lab has already been created in CS56-W14-Labs

1. cd into CS56-W14-Labs

2. ```git pull```

3. cd into github-acad-scripts and do:

 ```./updateForLab.py -g StudnetsGithubId -u githubAdminuser lab03```
 

 This will create the private repos ONLY for the single github id that is after -g, and ONLY if that githubid appears in the list in in the Google Doc referred to by GHA_STUDENT_LIST_URL


## Creating pair teams

1. ```. env.sh```  if not already done

2. ```./createPairTeams -g githubAdminUser```

You'll be prompted for password.

This should create all pair teams from the GHA_PAIR_TEAM_URL document.

## Creating repo for pair teams

1. ```. env.sh``` if not already done

2. ```./updatePairsForLab labxx -g githubAdminUser```

You'll be prompted for password

## Getting started---one-time steps

(1) clone the github-acad-scripts repo (scripts)
* via SSH <code>git clone git@github.com:UCSB-CS-Using-GitHub-In-Courses/github-acad-scripts.git</code>
* via HTTPS <code>git clone https://github.com/UCSB-CS-Using-GitHub-In-Courses/github-acad-scripts.git</code>
    
(2) cd into the github-acad-scripts repo and do:

```
git submodule init 
git submodule update
```
 This should populate the PyGithub and requests subdirectories with the contents of those "sub" repositories (those     are extra Python scripts from other authors, from other github repos, that our scripts depend on.)
 
(3) clone the CS56-W14-Labs repo (lab starting points)

* via SSH <code>git clone git@github.com:UCSB-CS56-W14/CS56-W14-Labs.git</code>
* via HTTPS <code>git clone https://github.com/UCSB-CS56-W14/CS56-W14-Labs.git</code>

(4) Copy the <code>env.sh.sample</code> to <code>env.sh</code> in your copy of the github-acad-scripts repo

cd back into your github-acad-scripts repo, and do this:

 ```cp env.sh.sample env.sh```
 
The file <code>env.sh</code> is NOT under github revision control---that's because it is designed to contain the "unpublished, obscure" URLs of the Google Documents that contain the class list.    Those are "sensitive", since the documents contain students' real names, email addresses, etc.  Therefore we don't want those URLs to be in a public repository.

(5) Edit your now local, private, <code>env.sh</code> to match the proper values (you can get those from your instructor, or whoever is setting up the Google Docs for your course.)


