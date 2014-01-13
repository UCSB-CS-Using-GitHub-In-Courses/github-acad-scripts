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

(4) Copy the env.sh.sample to env.sh in your copy of the github-acad-scripts repo\

cd back into your github-acad-scripts repo, and do this:

 cp env.sh.sample env.sh
 
The file <code>env.sh</code> is NOT under github revision control---that's because it is designed to contain the "unpublished, obscure" URLs of the Google Documents that contain the class list.    Those are "sensitive", since the documents contain students' real names, email addresses, etc.  Therefore we don't want those URLs to be in a public repository.

(5) Edit your now local, private, env.sh to match the proper values (you can get those from your instructor, or whoever is setting up the Google Docs for your course.)
