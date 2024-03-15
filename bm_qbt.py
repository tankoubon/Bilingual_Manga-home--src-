import json
import sys
import subprocess
import os

metadata_path = "json/"
torrent_name = "Bilingual Manga"
torrent_tar_ipfs_path = "Bilingual Manga/tar_ipfs/"

torrent_hash = None
torrent_properties = None
file_details = dict()

metadata = dict()
manga_titles = dict()
jp_chapters_per_id = dict()
en_chapters_per_id = dict()
en_synopsis_per_id = dict()

priority_txt = { 0: 'Do not download', 1:'Normal priority', 6:'High priority',7:'Maximal priority'}

def qbt_cmd(args):
    sp_args = ['qbt'] + args.split(' ')
    res = subprocess.run(sp_args,  capture_output=True, text=True)
    return res

"""
print("Getting qBittorrent client info:")
res = qbt_cmd("server info")
print(res.stdout)
"""

def refresh_qbt_status():
    global torrent_hash, torrent_properties, file_details
    print("Getting torrent listing")
    res = qbt_cmd('torrent list -F json')
    torrents = json.loads(res.stdout)

    for torrent in torrents:
        if torrent['name'] == torrent_name:
            torrent_hash = torrent['hash']

    if torrent_hash is None:
        print("Bilingual manga torrent not found on qBittorrent!")
        exit(1)
    else:
        print("Bilingual manga torrent hash: %s" % torrent_hash)

    print("Getting torrent info..")
    res = qbt_cmd('torrent properties %s -F json' % torrent_hash)
    torrent_properties = json.loads(res.stdout)

    print("Getting torrent content..")
    res = qbt_cmd('torrent content %s -F json' % torrent_hash)
    content = json.loads(res.stdout)
    for f in content:
        file_details[f['Name']] = f

print("Loading metadata..")
with open(metadata_path + "admin.manga_metadata.json","r", encoding="utf-8") as f:
    metadata = json.loads(f.read())
    titles = metadata[0]['manga_titles']
    for t_data in titles:
        title_id = t_data['enid']
        title = t_data['entit']
        manga_titles[title_id] = title

with open(metadata_path + "admin.manga_data.json","r",encoding="utf-8") as f:
    data = json.loads(f.read())
    for m in data:
        title_id = m['_id']['$oid']
        jp_chapter_ids = m['jp_data']['ch_jph']
        jp_chapters_per_id[title_id] = [cid.split('/')[0] for cid in jp_chapter_ids]
        en_chapter_ids = m['en_data']['ch_enh']
        en_chapters_per_id[title_id] = [cid.split('/')[0] for cid in en_chapter_ids]
        en_synopsis_per_id[title_id] = m['syn_en']

def extract_chapter(filename):
    if not os.path.exists('ipfs'):
        os.mkdir('ipfs')
    full_path = torrent_properties['SavePath'] + '/' + filename
    print("Extract from",full_path)
    sp_args = ['tar','xf',full_path,'--directory','ipfs']
    res = subprocess.run(sp_args, capture_output=True, text=True)
    if res.stderr != '':
        print(res.stderr)
    if res.stdout != '':
        print(res.stdout)
    else:
        print("ok")

def process(args):
    if len(args)>2:
        cmd = args[1]
        search_term = args[2].lower()

        print("Searching for %s" % search_term)
        chapter_ids = []
        for id, title in manga_titles.items():
            if search_term in title.lower():
                jp_ch = jp_chapters_per_id[id]
                en_ch = en_chapters_per_id[id]
                if cmd == 'search':
                    print("%s (%d jp and %d en chapters)" % (title,len(jp_ch),len(en_ch)))
                    print(en_synopsis_per_id[id])
                else:
                    print("Selected [%s] %s with %d jp and %d en chapters" % (id,title,len(jp_ch),len(en_ch)))
                chapter_ids += jp_ch
                chapter_ids += en_ch

        if len(chapter_ids) == 0:
            print("No such manga found!")
            exit(1)

        files = [torrent_tar_ipfs_path + ch + '.tar' for ch in chapter_ids]

        if cmd == 'search':
            exit(1)

        refresh_qbt_status()

        if cmd == 'status':
            for f in files:
                d = file_details[f]
                print("%.1f%% (%s) [%s]" % (d['Progress']*100, priority_txt[d['Priority']], f))
        elif cmd == 'download':
            for f in files:
                d = file_details[f]
                print("Setting %s to HIGH_PRIORITY" % f)
                res = qbt_cmd("torrent file priority -f %d -s 6 %s" % (d['Id'],torrent_hash))
                reply = res.stdout
                if reply == '':
                    reply = 'ok'
                print("\tReply: %s" % reply)
        elif cmd == 'extract':
            for f in files:
                d = file_details[f]
                if d['Progress'] != 1:
                    print("%s not yet fully complete (%.1f%%) so skipping extraction!" % (f,d['Progress']*100))
                else:
                    extract_chapter(f)

    else:
        print("Usage:")
        print("\tSearch for manga titles:")
        print("\t\tpython bm_qbt.py search <search_term> ")
        print("\t\tExample: python bm_qbt.py search akira")
        print("\tList download status of manga titles:")
        print("\t\tpython bm_qbt.py status <search_term> ")
        print("\t\tExample: python bm_qbt.py status akira")
        print("\tDownload manga titles:")
        print("\t\tpython bm_qbt.py download <search_term> ")
        print("\t\tExample: python bm_qbt.py download akira")
        print("\tExtract downloaded manga to IPFS folder:")
        print("\t\tpython bm_qbt.py extract <search_term> ")
        print("\t\tExample: python bm_qbt.py extract akira")

process(sys.argv)
