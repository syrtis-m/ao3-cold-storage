from AO3 import extra, utils
from AO3 import Chapter
from AO3 import Comment
from AO3 import common
from AO3 import Search
from AO3 import Series
from AO3 import GuestSession, Session
from AO3 import User
from AO3 import Work
import threading
import time
from bs4 import BeautifulSoup




def download_threaded(worklist):
        
    #slice into two lists
    middleindex = len(worklist)//2
    part1 = worklist[middleindex:]
    part2 = worklist[:middleindex]

    #define threads
    t1 = threading.Thread(target=download, args=(part1,))
    t2 = threading.Thread(target=download, args=(part2,))

    #start threads
    t1.start()
    t2.start()

    #threads end
    t1.join()
    t2.join()

    print("threaded download done")


def download(worklist):
    for fic in worklist:
        title = ''.join(filter(str.isalnum, fic.title)) #strip all but alphanumeric characters from the name of the fic
        try:
            fic.reload()
            fic.download_to_file("downloads/" + title + ".epub", filetype="EPUB")
            print("downloaded work:", title)
        except AttributeError:
            print("url returns 404 for work:", title)
            time.sleep(20)
    print("download done")


# some code in this object is taken from AO3_API licensed under a MIT license

def chunks(list, n):
    """Yield successive n-sized chunks from list."""
    for i in range(0, len(list), n):
        yield list[i:i + n]

class Downloader:
    def __init__(self, username, password, requests_per_min, bookmark_pause, download_pause):
        self.session = Session(username, password)
        self.user = User(username)
        self.user.set_session(self.session)
        utils.limit_requests() # limits the number of requests/minute
        utils.set_rqtw(requests_per_min)
        self.user.reload()
        self.bookmark_pause = bookmark_pause
        self.download_pause = download_pause
        print("url:", self.user.url)
        print("bio:", self.user.bio)
        print("works:", self.user.works)
        print("bookmarks:", self.user.bookmarks)

    def load_threaded_download_threaded(self):
        self.load_bookmarks_threaded() #threaded
        self.download_threaded(self.bookmarks) #threaded
        print("threaded download done")


    # load all bookmarks
    def load_bookmarks_threaded(self):            
        threads = []
        self.bookmarks = []
        #TODO add requests_per_min support
        for page in range(self.user._bookmarks_pages):
            k = page+1
            threads.append(threading.Thread(target=self.load_bookmarks_thread, args=(k,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    # single thread
    def load_bookmarks_thread(self, page=1):
        #from AO3.common import get_work_from_banner
        _soup_bookmarks = self.user.request(f"https://archiveofourown.org/users/{self.user.username}/bookmarks?page={page}") #TODO ERROR HERE
                
        ol = _soup_bookmarks.find("ol", {"class": "bookmark index group"})

        for work in ol.find_all("li", {"role": "article"}):
            time.sleep(self.bookmark_pause)
            authors = [] #not sure what this line does
            if work.h4 is None:
                continue
            self.bookmarks.append(common.get_work_from_banner(work))


    # downloaders
    def download_threaded(self, worklist):
        #worklist must be a list of Work objects

        worklist_parts_obj = chunks(worklist, 4)
        worklist_parts = list(worklist_parts_obj)

        threads = []
        for n in range(len(worklist_parts)):
            threads[n] = threading.Thread(target=self.download, args=(worklist_parts[n],))
            threads[n].start()

        for thread in threads:
            thread.join()

        """""
        #slice into two lists
        middleindex = len(worklist)//2
        part1 = worklist[middleindex:]
        part2 = worklist[:middleindex]

        #define threads
        t1 = threading.Thread(target=self.downloader, args=(part1,pause,))
        t2 = threading.Thread(target=self.downloader, args=(part2,pause,))

        #start threads
        t1.start()
        t2.start()

        #threads end
        t1.join()
        t2.join()
        """""


    def download(self, worklist):
        #worklist must be a list of Work objects

        for fic in worklist:
            title = ''.join(filter(str.isalnum, fic.title)) #strip all but alphanumeric characters from the name of the fic
            try:
                fic.reload()
                fic.download_to_file("downloads/" + title + ".epub", filetype="EPUB")
                time.sleep(self.download_pause)
                print("downloaded work:", title)
            except AttributeError:
                print("url returns 404 for work:", title)
        print("download done")