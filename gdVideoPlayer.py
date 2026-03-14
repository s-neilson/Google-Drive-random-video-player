import os
import asyncio
import random
from configurationFunctions import displayConfiguration,getImageFileTypes,getImageDuration
from synchronization import synchronizeFiles,getListOfLocalFiles



async def playRandomVideo(fileDeleteLock):
  while True:
    async with fileDeleteLock: #Ensures that videos are not played while files are being deleted.
      videoList=getListOfLocalFiles()
      if(len(videoList)==0):
        print("There are currently no videos to play")
        await asyncio.sleep(10) #Video playback will be tried again in 10 seconds.
        continue

      randomVideoPath=random.choice(getListOfLocalFiles())
      print("Now playing : "+randomVideoPath)

      ffplayString=""
      fileExtension=os.path.splitext(randomVideoPath)[1]
      if(fileExtension in getImageFileTypes()): #Images need to be treated differently to video files.
        frameCount=round(getImageDuration()*25.0) #The image is repeated for a certain amount of frames; assumes that the default FPS is 25.
        ffplayString="ffplay -loglevel error -fs -autoexit -loop "+str(frameCount)+" -i \""+randomVideoPath+"\""
      else:
        ffplayString="ffplay -loglevel error -fs -autoexit -i \""+randomVideoPath+"\""

      #Plays the video using ffplay in fullscreen. It will automatically exit when it ends.
      ffplaySubprocess=await asyncio.create_subprocess_shell(cmd=ffplayString)
      await ffplaySubprocess.wait()


async def mainLoop():
  displayConfiguration()

  fileDeleteLock=asyncio.Lock() #This lock prevents the possibility of a file being deleted while it is being played.
  videoDisplayTask=playRandomVideo(fileDeleteLock)
  synchronizationTask=synchronizeFiles(fileDeleteLock)
  await asyncio.gather(videoDisplayTask,synchronizationTask)



asyncio.run(mainLoop())





  