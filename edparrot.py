# ReceiveText
# When written: when a text message is received from another player or npc
# Parameters:
#    From
#    Message
#    Channel: (wing/local/voicechat/friend/player/npc/squadron/starsystem)

# Friends
# When written: when receiving information about a change in a friend's status
# Also written at startup for friends who are already online (new in v2.4)
# Parameters:
#    Status: one of the following: Requested, Declined, Added, Lost, Offline, Online
#    Name: the friend's commander name

import time
import json
import pathlib
import gtts
import glob
import os
import getpass
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from playsound import playsound

pathApp = str(pathlib.Path().resolve())
endLine = 0


def say(say_txt, x_lang):
    tts = gtts.gTTS(say_txt, lang=x_lang)
    tts.save("say.mp3")
    snd_file = pathApp + "\\say.mp3"
    playsound(snd_file)
    # print(gtts.lang.tts_langs())


def snd(snd_nr):
    snd_file = pathApp + '\\snd\\snd' + snd_nr + '.wav'
    playsound(snd_file)


class Event(LoggingEventHandler):
    def on_modified(self, event):
        global endLine
        if event.src_path.find("Journal") > 0:
            # print("[{}] noticed: [{}] on: [{}] ".format(time.asctime(), event.event_type, event.src_path))
            log_file = open(event.src_path, "r", encoding="utf-8")

            n_line = 0
            for log_line in log_file.readlines():
                n_line = n_line + 1

                if (n_line > endLine) and (log_line.find("ReceiveText") == 47):
                    endLine = n_line
                    po_line = json.loads(log_line)
                    ch = ''
                    if po_line['Channel'] != 'npc':
                        if po_line['Channel'] == 'friend':
                            ch = '<-F'
                        if po_line['Channel'] == 'squadron':
                            ch = '<-S'
                        if po_line['Channel'] == 'player':
                            ch = '<-P'
                        if po_line['Channel'] == 'wing':
                            ch = '<-W'
                        if po_line['Channel'] == 'local':
                            ch = '<-L'
                        if po_line['Channel'] == 'starsystem':
                            ch = '<-*'
                        print(po_line['timestamp'], "|", ch, po_line['From'], "|", po_line['Message'])
                        snd("5")
                        if (ch == '<-S') or (ch == '<-F') or (ch == '<-W'):
                            say(po_line['From'] + "powiedział:" + po_line['Message'], "pl")
                        else:
                            say(po_line['From'] + "powiedział:" + po_line['Message'], "en")

                if (n_line > endLine) and (log_line.find("SendText") == 47):
                    endLine = n_line
                    po_line = json.loads(log_line)
                    print(po_line['timestamp'], "| -->", po_line['To'], "|", po_line['Message'])

                if (n_line > endLine) and (log_line.find("Friends") == 47):
                    endLine = n_line
                    po_line = json.loads(log_line)
                    print(po_line['timestamp'], "| ###", po_line['Name'], "|", po_line['Status'])
                    if po_line['Status'] == 'Online':
                        snd("7")
                    if (po_line['Status'] == 'Offline') or (po_line['Status'] == 'Lost'):
                        snd("11")

            log_file.close()


if __name__ == "__main__":
    list_of_files = glob.glob(f"C:\\Users\\{getpass.getuser()}\\Saved Games\\Frontier Developments\\Elite Dangerous\\Journal.*")
    latestJournal = max(list_of_files, key=os.path.getmtime)
    path = glob.glob(f"C:\\Users\\{getpass.getuser()}\\Saved Games\\Frontier Developments\\Elite Dangerous")[0]
    path2 = latestJournal
    print(path2)

    logFile = open(path2, "r", encoding="utf-8")
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
