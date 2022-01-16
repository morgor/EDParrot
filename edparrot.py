#https://stackoverflow.com/questions/32923451/how-to-run-an-function-when-anything-changes-in-a-dir-with-python-watchdog
#https://pypi.org/project/deep-translator/
#https://medium.com/analytics-vidhya/how-to-translate-text-with-python-9d203139dcf5

##ReceiveText
##
##When written: when a text message is received from another player or npc
##
##Parameters:
##
##    From
##    Message
##    Channel: (wing/local/voicechat/friend/player/npc/squadron/starsystem)

##Friends
##
##When written: when receiving information about a change in a friend's status
##
##Also written at startup for friends who are already online (new in v2.4)
##
##Parameters:
##
##    Status: one of the following: Requested, Declined, Added, Lost, Offline, Online
##    Name: the friend's commander name


import sys
import time
import json
import pathlib
import gtts
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from playsound import playsound

pathApp = str(pathlib.Path().resolve())
endLine = 0

def say(sayTxt, xLang):
    tts = gtts.gTTS(sayTxt, lang=xLang)
    tts.save("say.mp3")
    snd = pathApp + '\say.mp3'
    playsound(snd)
    #print(gtts.lang.tts_langs())

def snd(sndNr):
    snd = pathApp + '\snd' + sndNr + '.wav'
    playsound(snd)

class Event(LoggingEventHandler):
    def on_modified(self, event):
        global endLine
        if (event.src_path.find("Journal") > 0):
            #print("[{}] noticed: [{}] on: [{}] ".format(time.asctime(), event.event_type, event.src_path))
            logFile = open(event.src_path,"r", encoding="utf-8")
            
            nLine = 0
            for line in logFile.readlines():
                nLine = nLine + 1

                if (nLine > endLine) and (line.find("ReceiveText") == 47):
                    endLine = nLine
                    poLine = json.loads(line)
                    if (poLine['Channel'] != 'npc'):
                        if (poLine['Channel'] == 'friend'): ch = '<-F'
                        if (poLine['Channel'] == 'squadron'): ch = '<-S'
                        if (poLine['Channel'] == 'player'): ch = '<-P'
                        if (poLine['Channel'] == 'wing'): ch = '<-W'
                        if (poLine['Channel'] == 'local'): ch = '<-L'
                        if (poLine['Channel'] == 'starsystem'): ch = '<-*'
                        print(poLine['timestamp'], "|", ch, poLine['From'], "|", poLine['Message'])
                        snd("5")
                        if (ch == '<-S') or (ch == '<-F') or (ch == '<-W'):
                            say(poLine['From'] + "powiedział:" + poLine['Message'], "pl")
                        else:
                            say(poLine['From'] + "powiedział:" + poLine['Message'], "en")

                if (nLine > endLine) and (line.find("SendText") == 47):
                    endLine = nLine
                    poLine = json.loads(line)
                    print(poLine['timestamp'], "| -->", poLine['To'], "|", poLine['Message'])

                if (nLine > endLine) and (line.find("Friends") == 47):
                    endLine = nLine
                    poLine = json.loads(line)
                    print(poLine['timestamp'], "| ###", poLine['Name'], "|", poLine['Status'])
                    if (poLine['Status'] == 'Online'): snd("7")
                    if (poLine['Status'] == 'Offline') or (poLine['Status'] == 'Lost'): snd("11")
                    
            logFile.close()
        

if __name__ == "__main__": 
    path = "C:\\Users\\test\\Saved Games\\Frontier Developments\\Elite Dangerous"
    path2 = path + "\\Journal.220116181554.01.log"

    logFile = open(path2,"r", encoding="utf-8")
    nLine = 0
    for line in logFile.readlines():
        nLine = nLine + 1
    logFile.close()
    endLine = nLine
            
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
