import AO3
import threading
import time

def downloader_threaded(worklist):
    #slice into two lists
    middleindex = len(worklist)//2
    part1 = worklist[middleindex:]
    part2 = worklist[:middleindex]

    #define threads
    t1 = threading.Thread(target=downloader, args=(part1,))
    t2 = threading.Thread(target=downloader, args=(part2,))

    #start threads
    t1.start()
    t2.start()

    #threads end
    t1.join()
    t2.join()

    print("threaded download done")


def downloader(worklist):
    for fic in worklist:
        title = ''.join(filter(str.isalnum, fic.title)) #strip all but alphanumeric characters from the name of the fic
        try:
            fic.reload()
            fic.download_to_file("downloads/" + title + ".epub", filetype="EPUB")
            print("downloaded work:", title)
        except AttributeError:
            print("url returns 404 for work:", title)
            time.sleep(20)
