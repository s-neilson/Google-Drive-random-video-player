import os
import yaml
import re



def getConfiguration():
  configurationFilePath=os.path.join(os.getcwd(),"configuration.yaml")
  configurationFile=open(configurationFilePath,mode="r")
  configurationData=list(yaml.safe_load_all(configurationFile))[0]
  configurationFile.close()
  return configurationData


def getFolderUrl():
  return getConfiguration()["folderUrl"]


def getResynchronizationTime():
  return getConfiguration()["resynchronizationTime"]


def getDeleteOldLocalFiles():
  return getConfiguration()["deleteOldLocalFiles"]


#Checks for invalid file extensions.
def checkFileExtensionsValid(fileTypes):
  invalidExtension=False

  for i in fileTypes:
    invalidExtension = invalidExtension or (len(i)<2) #Extension is zero or 1 characters
    invalidExtension = invalidExtension or (i[0]!=".") #Extension does not begin with period.
    invalidExtension = invalidExtension or (i[1]==".") #Period is second character in extension.
    invalidExtension = invalidExtension or ((i.find("/")!=-1) or (i.find("\\")!=-1)) #Extension has either a forward or backward slash.
    invalidExtension = invalidExtension or (i.find("*")!=-1) #Extension has an asterisk.
    invalidExtension = invalidExtension or (i.find(",")!=-1) #Extension has a comma.
    invalidExtension = invalidExtension or (i.find("|")!=-1) #Extension has a vertical bar.
    invalidExtension = invalidExtension or (re.search("\\s",i) is not None) #Extension has whitespace characters
    invalidExtension = invalidExtension or ((i.find("(")!=-1) or (i.find(")")!=-1)) #Extension has a round bracket.
    invalidExtension = invalidExtension or ((i.find("{")!=-1) or (i.find("}")!=-1)) #Extension has a curly bracket.
    invalidExtension = invalidExtension or ((i.find("[")!=-1) or (i.find("]")!=-1)) #Extension has a square bracket.
    invalidExtension = invalidExtension or ((i.find("<")!=-1) or (i.find(">")!=-1)) #Extension has a less than or greater than sign.
    invalidExtension = invalidExtension or ((i.find(":")!=-1) or (i.find(";")!=-1)) #Extension has a colon or semicolon.
    invalidExtension = invalidExtension or ((i.find("\"")!=-1) or (i.find("'")!=-1) or (i.find("`")!=-1)) #Extension has quotes or a backtick.

    if(invalidExtension):
      print("    \""+i+"\" is not a valid file extension")
      exit()


def getVideoFileTypes():
  return getConfiguration()["videoFileTypes"]


def getImageFileTypes():
  return getConfiguration()["imageFileTypes"]


def getFileTypes():
  return getVideoFileTypes()+getImageFileTypes()


def getImageDuration():
  return getConfiguration()["imageDuration"]
  
  
def getTryNotToRepeat():
  return getConfiguration()["tryNotToRepeat"]


def displayConfiguration():
  print("Current configuration: ")

  print("  Folder URL: "+getFolderUrl())
  print("  Time between resynchronizations: "+str(getResynchronizationTime())+" seconds")
  print("  Delete old local files: "+str(getDeleteOldLocalFiles()))

  print("  Video file types: ")
  videoFileTypes=getVideoFileTypes()
  checkFileExtensionsValid(videoFileTypes)
  for i in videoFileTypes:
    print("    "+i)

  print("  Image file types: ")
  imageFileTypes=getImageFileTypes()
  checkFileExtensionsValid(imageFileTypes)
  for i in imageFileTypes:
    print("    "+i)

  print("  Image duration: "+str(getImageDuration())+" seconds")
  print("")
  
  tryNotToRepeat=getTryNotToRepeat()
  if(tryNotToRepeat):
    print(" The program will attempt not to repeat media unless there is nothing more to play")
    print("")
  
