# Quick Reference for github-acad-scripts

Scripts for using github.com in Academic Courses

# Getting started

Do the one-time steps at the bottom of this document.

EACH TIME: run the script env.sh by typing 

 . env.sh
 
 





# Getting started---one-time steps

(1) clone the github-acad-scripts repo (scripts)

* via SSH <code>git clone git@github.com:UCSB-CS-Using-GitHub-In-Courses/github-acad-scripts.git</code>
* via HTTPS <code>git clone https://github.com/UCSB-CS-Using-GitHub-In-Courses/github-acad-scripts.git</code>
 
(2) cd into the github-acad-scripts repo and do:

 git submodule init
 git submodule update

This should populate the PyGithub and requests subdirectories with the contents of those "sub" repositories (those are extra Python scripts from other authors, from other github repos, that our scripts depend on.)


(3) clone the CS56-W14-Labs repo (lab starting points)

* via SSH <code>git clone git@github.com:UCSB-CS-Using-GitHub-In-Courses/github-acad-scripts.git</code>
* via HTTPS <code>git clone https://github.com/UCSB-CS-Using-GitHub-In-Courses/github-acad-scripts.git</code>

