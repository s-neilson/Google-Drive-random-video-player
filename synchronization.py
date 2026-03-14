import os
import asyncio
import glob
import gdown
from configurationFunctions import getFolderUrl,getResynchronizationTime,getDeleteOldLocalFiles,getFileTypes



def getListOfLocalFiles():
  videoPathList=[]
  for currentFileType in getFileTypes(): #Performs a glob search for each file type in the video download folder.
    globPattern=os.path.join(os.getcwd(),"videoDownloads","*"+currentFileType)
    videoPathList+=glob.glob(globPattern)
  return videoPathList


#The download folders are created if it doesn't already exist
def createDownloadFolders():
  videoFolder=os.path.join(os.getcwd(),"videoDownloads")
  if(not os.path.isdir(videoFolder)):
    print("Creating video download folder")
    print("")
    os.mkdir(videoFolder)


#Returns list of compatible files that exist in a Google Drive folder.
def getListOfRemoteFiles():
  folderUrl=getFolderUrl()
  print("Getting list of compatible files in Google Drive folder \""+folderUrl+"\"")
  videoFolder=os.path.join(os.getcwd(),"videoDownloads")
  filesToDownload=gdown.download_folder(url=folderUrl,quiet=True,output=videoFolder,skip_download=True)

  fileListVideo=[]
  for i in filesToDownload: #Only files with specific extensions are returned.
    fileExtension=os.path.splitext(i.local_path)[1]

    validFileExtensions=getFileTypes()
    if(fileExtension in validFileExtensions):
      fileListVideo.append(i)

  return fileListVideo


#Returns a list of files to be downloaded
def getVideosToChange(remoteFileListVideo):
  print("Getting list of existing local video files: ")
  localVideos=getListOfLocalFiles()
  for i in localVideos:
    print("  "+i)
  print("")

  fileNamesToDownload=[]
  fileNamesToDelete=[]

  #Finds remote files that are not currently in the local folder. These files will be downloaded.
  for i in remoteFileListVideo:
    remoteFilePath=i.local_path
    if(remoteFilePath not in localVideos):
      fileNamesToDownload.append((remoteFilePath,i.id)) #Also includes the Google Drive file Id.

  print("Files to download: ")
  for i in fileNamesToDownload:
    print("  "+i[0])
  print("")

  #Finds local files not in the remote folder. These files will be deleted if getDeleteOldLocalFiles()=True  
  if(getDeleteOldLocalFiles()):
    remoteFilePaths=[i.local_path for i in remoteFileListVideo]      
    for i in localVideos:
      if(i not in remoteFilePaths):
        fileNamesToDelete.append(i)  

    print("Old local files to delete: ")
    for i in fileNamesToDelete:
      print("  "+i)
    print("")
  else:
    print("Old local files will not be deleted")
    print("")

  return fileNamesToDownload,fileNamesToDelete


async def deleteOldLocalFiles(fileNamesToDelete,fileDeleteLock):
  if(len(fileNamesToDelete)>0):
    async with fileDeleteLock: #Ensures that files are not deleted while a video is being played.
      print("Deleting old local files: ")
      for i in fileNamesToDelete:
        print("  Deleting "+i)
        os.remove(i)
    print("")
     

async def downloadVideos(fileNamesToDownload):
  print("Downloading "+str(len(fileNamesToDownload))+" videos")
  videoFolder=os.path.join(os.getcwd(),"videoDownloads")
  
  for currentFile in fileNamesToDownload:
    await asyncio.sleep(0.1) #Allows, if needed, a new video to start playing before the download begins.
    gdown.download(id=currentFile[1],resume=True,output=currentFile[0])
  print("")


async def synchronizeFiles(fileDeleteLock):
  while True:
    print("Synchronizing files")
    createDownloadFolders()
    remoteVideoList=getListOfRemoteFiles()
    videoFilesToDownload,videoFilesToDelete=getVideosToChange(remoteVideoList)

    await downloadVideos(videoFilesToDownload)
    #downloadFunction=lambda : downloadVideos(videoFilesToDownload)
    #await asyncio.get_running_loop().run_in_executor(None,downloadFunction)

    await deleteOldLocalFiles(videoFilesToDelete,fileDeleteLock)
    print("")

    await asyncio.sleep(getResynchronizationTime()) #A specified time is waited before resynchonizing again.