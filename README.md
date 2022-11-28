# cold-storage
a jupyter notebook to mass-download your ao3 bookmarks. 

## details
- this is a work in progress - things may be broken. updates are posted on cohost under the tag `#syrtis_dev`
- downloads are formatted as if you had downloaded them from ao3 manually.
- downloads are currently formatted as .epub files


## usage
1. run `pip install ao3_api` in your shell
2. if you don't have a jupyter client, run `pip install notebook` in your shell
3. git clone this repo, or download `cold_storage.ipynb`
4. create a file in the same folder as `cold_storage.ipynb` called `secret.py`
5. in `secret.py` create the following with your ao3 username and password. this allows the downloader to grab private bookmarks.
```python
username = ""
password = ""
```
6. run each cell in `cold_storage.ipynb`. some cells may take a while to run. fics should show up in yout
