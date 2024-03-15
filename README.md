# Bilingual_Manga offline (source)

Sadly bilingualmanga.org is not functional anymore. This repository contains updated instructions
how to nevertheless continue using the offline version on your computer:

1. Get the database json files from https://github.com/tankoubon/Bilingual_Manga_databases and place them in json folder. Use the version modified for 100% offline use

2. Fetch the Bilingual Manga torrent file from the repository above


##### Option 1. Install whole manga catalog
If you don't mind the 700+GB download then just download the whole torrent
 - Unzip all the downloaded tar files in _tar_ipfs/_ folder into _ipfs/_ folder such that its content looks like 
   ```
   ipfs/bafybeihz7gz4qhqjrck33cbmpa3mr7ouh3ztw6cr64conje2h2zynrboki/
   ....
    ```
   
##### Option 2. Select few manga titles

In case you just want few selected manga titles you can use the following steps:

 - Use qBittorrent to start the download but skip the _tar_ipfs/_ folder. It's preferable to use separate directory for incomplete files.
 - Enable qBittorrent Remote control:  Tools -> Preferences -> Web UI -> Enable "Web User Interface" and "Bypass authentication for clients on localhost". If you want authentication (for example if you have a remote qBittorrent server) you need to modify the download script yourself
 - Install the qBittorrent command line client: https://github.com/fedarovich/qbittorrent-cli/wiki
 - Make sure that python 3+ is installed
    ```
    python -V
    ```
 - You can browse the catalog:
    ```
    python bm_qtb.py search akira
    Loading metadata..
    Searching for akira
    Akira (6 jp and 6 en chapters)
    ....
     ```
  - Then start the download:
    ```
    python bm_qtb.py download akira
    ```
 - You may have to manually do *Force resume* on GUI if needed
 - You can check the download status (or just use qBittorrent GUI, but it has so many files..):
    ```
    python bm_qtb.py status akira
    ```
- When the download is finished you can extract the files into the _ipfs/_ folder:
    ```
    python bm_qtb.py extract akira
    ```


#### Few more steps..
4.  Copy the rest of the files (ocr.zip, wp-content/ and manga_cover/) from the torrent into the current directory and unzip also ocr.zip


5. Get the Node.js from https://nodejs.org/en/download (version 20.11.1 recommended)
 - Make sure the correct version is installed:
    ```
    node -v
    v20.11.1
    ```

6. Run these commands in the main directory
- `npm install`
- `node app.js`
- `npm run dev`

7. Go to http://localhost:5173 and enjoy!
