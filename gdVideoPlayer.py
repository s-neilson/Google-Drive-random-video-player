import os
import asyncio
import random
from configurationFunctions import displayConfiguration,getImageFileTypes,getImageDuration,getTryNotToRepeat
from synchronization import synchronizeFiles,getListOfLocalFiles



async def playRandomVideo(fileDeleteLock,playedMedia):
  while True:
    async with fileDeleteLock: #Ensures that videos are not played while files are being deleted.
      videoList=getListOfLocalFiles()
      if(len(videoList)==0):
        print("There are currently no videos to play")
        await asyncio.sleep(10) #Video playback will be tried again in 10 seconds.
        continue

      mediaToPlay=getListOfLocalFiles()
      if(getTryNotToRepeat()):
        mediaToPlay=list(set(getListOfLocalFiles()).difference(set(playedMedia)))
        if(len(mediaToPlay)==0):
          print("There is no more unplayed media, resetting list of played media")
          playedMedia=[]
          mediaToPlay=getListOfLocalFiles()
        
      randomVideoPath=random.choice(mediaToPlay)
      print("Now playing : "+randomVideoPath)
      playedMedia.append(randomVideoPath)

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
  playedMedia=[] #Holds a list of the media that has already been played.

  fileDeleteLock=asyncio.Lock() #This lock prevents the possibility of a file being deleted while it is being played.
  videoDisplayTask=playRandomVideo(fileDeleteLock,playedMedia)
  synchronizationTask=synchronizeFiles(fileDeleteLock,playedMedia)
  await asyncio.gather(videoDisplayTask,synchronizationTask)



asyncio.run(mainLoop())





  
