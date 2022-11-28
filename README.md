# ao3-cold-storage
a jupyter notebook to mass-download your ao3 bookmarks. 

## details
- this is a work in progress - things may be broken. updates are posted on cohost under the tag `#syrtis_dev`
- downloads are formatted as if you had downloaded them from ao3 manually.
- downloads are currently formatted as .epub files
- it takes roughly 104 minutes to download 500 fics. just let it run in the background


## usage
1. install
    - run `pip install ao3_api` in your shell
    - if you don't have a jupyter client, run `pip install notebook` in your shell
    - git clone this repo, or download `cold_storage.ipynb`
2. config 
    - create a file in the same folder as `cold_storage.ipynb` called `secret.py`
    - in `secret.py` create the following with your ao3 username and password. this allows the downloader to grab private bookmarks.
    ```python
    username = ""
    password = ""
    ```
3. run
    - run each cell in `cold_storage.ipynb`
    - wait. the notebook will give you a download time estimate, but as a rule of thumb you can download 140 works every 30 minutes. make a cup of hot cocoa, watch a show, read something.