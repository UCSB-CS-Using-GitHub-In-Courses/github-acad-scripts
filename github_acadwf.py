# github-acadwf.py contains utility functions for 
# working with PyGithub objects to set up teams, and repositories
# and other Github objects for academic workflows.

from __future__ import print_function
import sys
import os

def getenvOrDie(env,msg):
   result = os.environ.get(env)

   if result==None:
      print(msg)
      sys.exit()

   return result


def populateRepo(repo,protoDir,scratchDir):
    import subprocess
    callList = ["./populateRepo.sh",repo.name,repo.ssh_url,protoDir,scratchDir]
    print ("Calling " + " ".join(callList))
    subprocess.call(callList)

def resetRepoShell(repo,protoDir,scratchDir):
    import subprocess
    callList = ["./resetRepo.sh",repo.name,repo.ssh_url,protoDir,scratchDir]
    print ("Calling " + " ".join(callList))
    subprocess.call(callList)


def pullRepoForGrading(repo,gradingDir):
    import subprocess
    callList = ["./pullRepoForGrading.sh",repo.name,repo.ssh_url,gradingDir]
    print ("Calling " + " ".join(callList))
    subprocess.call(callList)

def pushFilesToRepo(g,org,lab,githubid,scratchDirName,startPointDir):

    addPyGithubToPath()
    from github import GithubException

    import os

    protoDirName = startPointDir + "/" + lab
    
    # check to see if protoDirName exists.  If not, bail
    
    if (not os.path.isdir(protoDirName)):
        raise Exception(protoDirName + " does not exist.")

    if (not os.path.isdir(scratchDirName)):
        raise Exception(scratchDirName + " does not exist.")

    protoDirName = os.path.abspath(protoDirName)
    scratchDirName = os.path.abspath(scratchDirName)

    if (githubid!=""):
        try:
            repoName = (lab + "_" + githubid)
            repo = org.get_repo(repoName)
            populateRepo(repo,protoDirName,scratchDirName)
        except GithubException as ghe:
            print("Could not find repo " + repoName + ":" + str(ghe))
            
    else:
            
        # User wants to update ALL repos that start with labxx_
        
        repos = org.get_repos()
        for repo in repos:
            if (repo.name.startswith(lab+"_")):
                populateRepo(repo,protoDirName,scratchDirName)
            

def resetFilesInRepo(g,org,lab,githubid,scratchDirName,startPointDir):

    addPyGithubToPath()
    from github import GithubException

    import os

    protoDirName = startPointDir + "/" + lab
    
    # check to see if protoDirName exists.  If not, bail
    
    if (not os.path.isdir(protoDirName)):
        raise Exception(protoDirName + " does not exist.")

    if (not os.path.isdir(scratchDirName)):
        raise Exception(scratchDirName + " does not exist.")

    protoDirName = os.path.abspath(protoDirName)
    scratchDirName = os.path.abspath(scratchDirName)

    if (githubid!=""):
        try:
            repoName = (lab + "_" + githubid)
            repo = org.get_repo(repoName)
            populateRepo(repo,protoDirName,scratchDirName)
        except GithubException as ghe:
            print("Could not find repo " + repoName + ":" + str(ghe))
            
    else:
            
        # User wants to update ALL repos that start with labxx_
        
        repos = org.get_repos()
        for repo in repos:
            if (repo.name.startswith(lab+"_")):
                restRepoShell(repo,protoDirName,scratchDirName)
            


def pushFilesToPairRepo(g,org,lab,team,scratchDirName,startPointDir):

    addPyGithubToPath()
    from github import GithubException

    import os

    protoDirName = startPointDir + "/" + lab
    
    # check to see if protoDirName exists.  If not, bail
    
    if (not os.path.isdir(protoDirName)):
        raise Exception(protoDirName + " does not exist.")

    if (not os.path.isdir(scratchDirName)):
        raise Exception(scratchDirName + " does not exist.")

    protoDirName = os.path.abspath(protoDirName)
    scratchDirName = os.path.abspath(scratchDirName)

    
    try:
        repoName = (lab + "_" + team.name)
        repo = org.get_repo(repoName)
        populateRepo(repo,protoDirName,scratchDirName)
    except GithubException as ghe:
        print("Could not find repo " + repoName + ":" + str(ghe))
            



def addPyGithubToPath():
    pathToPyGithub="./PyGithub";
    if not pathToPyGithub in sys.path:
        sys.path.append("./PyGithub")


def addStudentsFromFileToTeams(g,org,infileName):
    
    addPyGithubToPath()
    
    userList = getUserList(infileName)
    
    for line in userList:
        print("adding " + line['first'] + " " + line['last'])
        studentTeam = addStudentToTeams(g,org,
                          line['last'],
                          line['first'],
                          line['github'],
                          line['email'],
                          line['csil'])

def updateStudentsFromFileForLab(g,org,infileName,lab,scratchDirName,startPointDir,force,githubid=''):

    """
    firstName='' means updateAllStudents
    """

    addPyGithubToPath()
    
    userList = getUserList(infileName)

    for line in userList:
        
        if ( githubid=="" or line['github']==githubid ):
        
            studentTeam = addStudentToTeams(g,org,
                                       line['last'],
                                       line['first'],
                                       line['github'],
                                       line['email'],
                                       line['csil'])
            
            result = createLabRepoForThisUser(g,org,lab,
                                              line['last'],line['first'],
                                              line['github'],
                                              line['email'],line['csil'],
                                              studentTeam)
            

            if (result or force):
               pushFilesToRepo(g,org,lab,line['github'],scratchDirName,startPointDir)

            updateLabRepoForThisUser( g,org,lab,
                                      line['last'],line['first'],
                                      line['github'],
                                      line['email'],line['csil'],
                                      studentTeam)
               

def resetRepo(g,org,infileName,lab,scratchDirName,startPointDir,githubid):

    addPyGithubToPath()
    
    userList = getUserList(infileName)

    for line in userList:
        
        if ( githubid=='' or  line['github']==githubid ):
        
            studentTeam = addStudentToTeams(g,org,
                                       line['last'],
                                       line['first'],
                                       line['github'],
                                       line['email'],
                                       line['csil'])
            
            result = createLabRepoForThisUser(g,org,lab,
                                              line['last'],line['first'],
                                              line['github'],
                                              line['email'],line['csil'],
                                              studentTeam)
            
            if (not result):
               updateLabRepoForThisUser( g,org,lab,
                                              line['last'],line['first'],
                                              line['github'],
                                              line['email'],line['csil'],
                                              studentTeam)

            resetFilesInRepo(g,org,lab,line['github'],scratchDirName,startPointDir)
                
        

def updateAllStudentsFromFileForLab(g,org,infileName,lab,scratchDirName):

    
    addPyGithubToPath()
    
    userList = getUserList(infileName)

    for line in userList:
        
        studentTeam = addStudentToTeams(g,org,
                                       line['last'],
                          line['first'],
                          line['github'],
                          line['email'],
                          line['csil'])

        result = createLabRepoForThisUser(g,org,lab,
                                 line['last'],line['first'],line['github'],
                                 line['email'],line['csil'],
                                 studentTeam)
        
        if (result):
            pushFilesToRepo(g,org,lab,line['first'],scratchDirName,startPointDir)


def addUserToTeam(team,user,quiet=False):
    "A wrapper for team.add_to_members(user).  Returns true on success"

    addPyGithubToPath()
    from github import GithubException

    try:
       team.add_to_members(user)
       if not quiet:
           print(
           "user {0} added to {1}...".format( user.login, team.name) , end='')
       return True
    except GithubException as e:
       print (e)
       
    return False


def addStudentToTeams(g,org,lastName,firstName,githubUser,email,csil):
    """
    return the team if it was created or found, and user is member 
    Otherwise False
    Only creates team and adds if wasn't already on the teams
    """

    print("addStudentToTeams: {0} {1} (github: {2})...".format(
            firstName,lastName,githubUser),end='')

    studentTeam = getStudentTeam(org, githubUser)

    if (studentTeam != False):
        print("Team {0} exists...".format(studentTeam.name),end='')
    else:
        studentTeam = createTeam(org,
                                 formatStudentTeamName(githubUser))
    

    studentGithubUser = findUser(g,githubUser)
    if (studentGithubUser == False):
        print ("github user {0} for {1} {2} does not exist".format(githubUser,firstName,lastName))
        return False       

    result = addUserToTeam(studentTeam,studentGithubUser,quiet=False)

    if (result):
        result = addUserToTeam(
            getAllStudentsTeam(org),studentGithubUser,quiet=False)
        return studentTeam
    else:
        return False
               
def  getStudentTeam(org,githubUser,refresh=False):
    return findTeam(org,formatStudentTeamName(githubUser),refresh)

def  getAllStudentsTeam(org,refresh=False):
    return findTeam(org,"AllStudents",refresh)

    


def createStudentFirstNameTeamAndAddStudent(g,org,
                                       lastName,firstName,
                                       githubUser,email,csil):
    addPyGithubToPath()
    from github import GithubException

    print(firstName + " " + lastName + "...",end='');

    user = findUser(g,githubUser)

    if (user==False):
       return

    team = createTeam(org,
                      formatStudentTeamName(githubUser))
    if (team==False):
       return

def addStudentToAllStudentsTeam(g,
                                org,
                                lastName,
                                firstName,
                                githubUser,
                                email,csil):

    addPyGithubToPath()
    from github import GithubException

    user = findUser(g,githubUser)

    if (user==False):
       return
    
    # TRY ADDING STUDENT TO THE AllStudents team

    try:
        allStudentsTeam = findTeam(org,"AllStudents");
        if (allStudentsTeam != False):
           allStudentsTeam.add_to_members(user);
           print("... {0}({1}) added to AllStudents\n".format(firstName,githubuser))

    except GithubException as e:
       print (e)

def createLabRepo(g,org,infileName,lab):


    userList = getUserList(infileName)

    for line in userList:
        createLabRepoForThisUser(g,
                                 org,
                                 lab,
                                 line['last'],
                                 line['first'],
                                 line['github'],
                                 line['email'],
                                 line['csil'])
        

def createLabRepoForThisUser(g,
                             org,
                             lab,
                             lastName,firstName,githubUser,email,csil,
                             team=False):
   

    print(firstName + "\t" + lastName + "\t" + githubUser);
    
    githubUserObject = findUser(g,githubUser)

    if (githubUserObject == False):
        print("ERROR: could not find github user: " + githubUser);
        return False

    teamName = formatStudentTeamName(githubUser)

    if (team==False):
        team = findTeam(org,teamName);

    if (team==False):
        team = findTeam(org,teamName,refresh=True);

    if (team == False):
        print("ERROR: could not find team: " + teamName)
        print("RUN THE addStudentsToTeams script first!")
        return False
    
    return createRepoForOrg(org,lab,
                            githubUserObject,team,firstName,lastName,githubUser,csil)


def updateLabRepoForThisUser(g,
                             org,
                             lab,
                             lastName,firstName,githubUser,email,csil,
                             team=False):
   

    print(firstName + "\t" + lastName + "\t" + githubUser);
    
    githubUserObject = findUser(g,githubUser)

    if (githubUserObject == False):
        print("ERROR: could not find github user: " + githubUser);
        return False

    teamName = formatStudentTeamName(githubUser)

    if (team==False):
        team = findTeam(org,teamName);

    if (team==False):
        team = findTeam(org,teamName,refresh=True);

    if (team == False):
        print("ERROR: could not find team: " + teamName)
        print("RUN THE addStudentsToTeams script first!")
        return False
    
    return updateRepoForOrg(org,lab,
                            githubUserObject,team,firstName,lastName,githubUser,csil)

    
def formatRepoDesc(labNumber,firstName,lastName):

    GHA_GITHUB_ORG = getenvOrDie("GHA_GITHUB_ORG",
                        "Error: please set GHA_GITHUB_ORG to name of github organization for the course, e.g. UCSB-CS56-W14")

    desc = labNumber + " for " + firstName + " " + lastName
    return desc



def createRepoForOrg(org,labNumber,githubUserObject,githubTeamObject, firstName,lastName,githubid,csil):

    addPyGithubToPath()
    from github import GithubException

    desc = formatRepoDesc(labNumber,firstName,lastName)
    repoName =            labNumber + "_" + githubid  # name -- string
    try:  
        repo = org.create_repo(
            repoName,
            desc,
            "http://www.cs.ucsb.edu/~" + csil, # homepage -- string
            True, # private -- bool
            True, # has_issues -- bool
            True, # has_wiki -- bool
            True, # has_downloads -- bool
            team_id=githubTeamObject,
            auto_init=True,
            gitignore_template="Java")
        print(" Created repo "+repoName)
        return True
    except GithubException as e:
       if 'errors' in e.data and 'message' in e.data['errors'][0] and e.data['errors'][0]['message']=='name already exists on this account':
           print(" repo {0} already exists".format(repoName))
       else:
           print (e)

    return False


def updateRepoForOrg(org,labNumber,githubUserObject,githubTeamObject, firstName,lastName,githubid,csil):

    addPyGithubToPath()
    from github import GithubException

    desc = formatRepoDesc(labNumber,firstName,lastName)
    repoName =            labNumber + "_" + githubid  # name -- string
    try:  
        repo = org.get_repo(repoName);

        repo.edit(repoName,
                  description=desc, # description 
                  homepage="http://www.cs.ucsb.edu/~" + csil) # homepage -- string
        print("Updated repo "+repoName)
        return True
    except GithubException as e:
       print ("Error editing repo: " + repoName + " : " + e)

    return False


def findUser(g,githubUser,quiet=False):
    "wraps the get_user method of the Github object"

    addPyGithubToPath()
    from github import GithubException

    try:
        user = g.get_user(githubUser)
        if (user == None):
            if not quiet:
                print("No such github user: ",githubUser)
            return False
        else:
            if not quiet:
                print(" githubUser: " + user.login + "...",end='');
            return user
    except GithubException as e:
        print(e)
        if not quiet:
            print("No such github user: ",githubUser);
        return False

def formatStudentTeamName(githubUser):
       return "Student_" + githubUser  # name -- string


def createTeam(org,teamName,quiet=False):
    """
    Only creates the team---doesn't add any members.
    Returns the created team.
    If team already exists, returns reference to that team object.
    Returns False if team can't be created and can't be found.
    """

    addPyGithubToPath()
    from github import GithubException

    # Try to create the team

    team = False   # Sentinel to see if it succeeded or failed
    try:
       team = org.create_team(teamName,
                         [],
                         "push");
       if team!=False:
           if not quiet:
               print(" team {0} created...".format(teamName),end='')
           return team
    except GithubException as e:
       
       if ('errors' in e.data and e.data['errors'][0]['code']=='already_exists'):
          if not quiet:
              print(" team {0} already exists...".format(teamName),
                         end='') 
       else:
          print (e)
       
    # If the create failed, try to find the team by name
    # This is our own function and does NOT throw an exception on failure

    team = findTeam(org,teamName)
    if team!=False:
        return team

    team = findTeam(org,teamName,refresh=True)
    if team!=False:
        return team
     
    if not quiet:
        print(
            "ERROR: team {0} could not be created and was not found".format(
                teamName))
        
    return False
        
    

def findTeam(org,teamName,refresh=False):

    # There isn't a "lookup team by name within an org"
    # function in the API.  So we cache a dictionary of teams
    # on the first call, then use that afterwards to look up the team.
            
    if (not hasattr(findTeam, 'cacheTeamList')) or refresh:
        findTeam.cacheTeamList = org.get_teams();

    if (not hasattr(findTeam, 'cacheTeamDict')) or refresh:
        findTeam.cacheTeamDict = {}

        for team in findTeam.cacheTeamList:
            findTeam.cacheTeamDict[team.name]=team

    if teamName in findTeam.cacheTeamDict:
        return findTeam.cacheTeamDict[teamName]
    
    return False


def addTeamsForPairsInFile(g,org,studentFileName,pairFileName):
    
    #addPyGithubToPath()
    
    userList = getUserList(studentFileName)

    pairList = getPairList(userList,pairFileName)
    
    for pair in pairList:
        print("\nCreating team {0}...".format(pair["teamName"]))
        pairTeam = createTeam(org,pair["teamName"])
        user1 = findUser(g,pair["user1"]["github"])
        if (user1==False):
            raise Exception("Could not find github user {0}".pair["user1"]["github"])

        addUserToTeam(pairTeam,user1)
        user2 = findUser(g,pair["user2"]["github"])
        if (user2==False):
            raise Exception("Could not find github user {0}".pair["user2"]["github"])
        addUserToTeam(pairTeam,user2)
        

    

def updatePairsForLab(g,org,lab,scratchDirName,startPointDir,prefix=""):

    """
    go through all Pair_First1_First2 teams and create a repo for each one for this
    lab
    """

    addPyGithubToPath()

    allTeams = org.get_teams()

    # If user didn't pass in prefix, then make teams for ALL pairs,
    # that is, every team that starts with Pair_  otherwise,
    # make for every team that starts with prefix

    startsWith =  ("Pair_" if (prefix=="") else prefix)
    
    for team in allTeams:
        
        if team.name.startswith(startsWith):
            print("\nTeam: " + team.name,end='')
            result = createLabRepoForThisPairTeam(g,org,lab,team)
            

            pushFilesToPairRepo(g,org,lab,team,scratchDirName,startPointDir)
                
        


def createLabRepoForThisPairTeam(g,
                             org,
                             lab,
                             team):

    print("Creating repo for " + team.name + "...",end='')
    
    return createRepoForPairTeam(org,lab,team)

def createRepoForPairTeam(org,labNumber,team):

    addPyGithubToPath()
    from github import GithubException


    desc = "Github repo for " + labNumber + " for " + team.name
    repoName = labNumber + "_" + team.name  # name -- string
    try:  
        repo = org.create_repo(
            repoName,
            labNumber + " for " + team.name, # description 
            "http://www.cs.ucsb.edu/~pconrad/cs56", # homepage -- string
            True, # private -- bool
            True, # has_issues -- bool
            True, # has_wiki -- bool
            True, # has_downloads -- bool
            team_id=team,
            auto_init=True,
            gitignore_template="Java")
        print(" Created repo "+repoName)
        return True
    except GithubException as e:
       if 'errors' in e.data and 'message' in e.data['errors'][0] and e.data['errors'][0]['message']=='name already exists on this account':
           print(" repo {0} already exists".format(repoName))
       else:
           print (e)

    return False


def getUserList(csvFilename):

    import csv

    with open(csvFilename,'r') as f:
        csvFile = csv.DictReader(f,delimiter=',', quotechar='"')
    
        userList = convertUserList(csvFile)
        
        return userList
    
def convertUserList(csvFile):
    userList = []
    for line in csvFile:
        userList.append(makeUserDict(line["First Name"],
                                     line["Last Name"],
                                     line["github userid"],
                                     line["Umail address"],
                                     line["CSIL userid"]))
    

    return userList

def makeUserDict(first,last,github,email,csil):
    return {'first': first, 'last': last, 'github': github.lower(), 'email':email.lower(), 'csil':csil.lower() }

def getCSVFromURL(url, workdir, filename, message=""):

   if not os.access(workdir, os.W_OK):
      print(workdir + " is not a writeable scratch directory; " + message)
      sys.exit()

   sys.path.append("requests");

   import requests
   response = requests.get(url + '&output=csv')
   assert response.status_code == 200, 'Wrong status code'

   csvFile = workdir + "/" + filename

   with open(csvFile, 'w') as f:
      print (response.content,file=f)

   print("retrieved CSV file from URL")
   
   return csvFile

def getPairList(userList,csvFilename):
   
   import csv

   with open(csvFilename,'r') as f:
      csvFile = csv.DictReader(f,delimiter=',', quotechar='"')
      
      pairList = convertPairList(userList,csvFile)
      
      return pairList
   
def convertPairList(userList,csvFile):
    """
    userList is a list of dictionaries with keys first,last,github,email,csil
    csvFile is a list of dictionaries with keys Partner1_GithubID,Partner2_GithubID,labnumber
    
    returned value should be a list of dictionaries with keys teamName,user1,user2, where user1 and user2 are the elements fromn userlist where the github ids match.
    """

    pairList = []
    userLookupDict = makeUserLookupDictByGithubId(userList)
    for line in csvFile:
        line['Partner1_GithubID']=line['Partner1_GithubID'].lower().strip()
        line['Partner2_GithubID']=line['Partner2_GithubID'].lower().strip()
        if not (line['Partner1_GithubID'] in userLookupDict):
            raise Exception("Partner1_GithubID from pair file not found in user list: {0}".format(line['Partner1_GithubID']))
        
        if not (line['Partner2_GithubID'] in userLookupDict):
            raise Exception("Partner2_GithubID from pair file not found in user list: {0}".format(line['Partner2_GithubID']))
        
        team = {}
        user1 = userLookupDict[line['Partner1_GithubID']]
        user2 = userLookupDict[line['Partner2_GithubID']]
        if (user1["github"] > user2["github"]): 
            # Swap if out of order
            temp = user1
            user1 = user2
            user2 = temp
        team["user1"] = user1
        team["user2"] = user2
        team["teamName"]="Pair_" + user1['github'] + "_" + user2['github']
        
        pairList.append(team)
        
    return pairList

def makeUserLookupDictByGithubId(userList):
    """
    userList is a list of dictionaries with keys first,last,github,email,csil.
    returned value is a dictionary where the keys are the github ids,
      and the values are the original dictionaries with first,last,github,email,csil
    """

    newDict = {}
    for user in userList:
        if user['github'] in newDict:
            raise Exception("duplicate github user {0}".format(user['github']))
        newDict[user['github']]=user

    return newDict

def pullRepoForGrading(repo,gradingDir):
    import subprocess
    callList = ["./pullRepoForGrading.sh",repo.name,repo.ssh_url,gradingDir]
    print ("Calling " + " ".join(callList))
    subprocess.call(callList)
