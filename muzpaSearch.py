import requests, json, sys, time, random

headers = {
    'Cookie': "SESS=6fb6428329bddc27c87f31871270f6c715bc53",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "srv.muzpa.com",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

headersOld = {
    'Cookie': "SESS=6fb6428329bddc27c87f31871270f6c715bc53",
    # 'Content-Type': "text/plain",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "srv.muzpa.com",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "40",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

def search(aristName):
    url = "https://srv.muzpa.com/a/ms/media/search"

    # querystring = {"mp3prefered":"false","page":"0","popular_order":"false","text":"%5C.Dj+Tennis%5Cs"}
    querystring = {"mp3prefered":"false","page":"0","popular_order":"false","text":aristName}

    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
    responseJson = json.loads(response.text)
    # print '\n\n\n'
    
    lowCount = 1000
    artistIds = []

    albums = responseJson['albums']
    if albums: 
        for album in albums:
            tracks = album['tracks']
            if tracks:
                for track in tracks:
                    # if artistName in track['filename']:
                    # print track['artist']
                    if matchArtist(track['artist'], aristName) > -1:
                        # print track['artist']
                        artistsOnTracks = track['artists_ids']
                        al = len(artistsOnTracks)
                        # print al
                        if al < lowCount:
                            artistIds = artistsOnTracks
        
    # print artistIds
    return artistIds


def matchArtist(search, input):
    if search is None or input is None:
        return False

    searchEncoded = search.encode('utf-8')
    # print "search " + searchEncoded + " input " + input
        
    hit = searchEncoded.lower().find(input.lower())
    # print hit
    return hit


allSubResponses = []

def sub(id):

    url = "https://srv.muzpa.com/a/ms/artists_subscribes"

    # payload = "{\"artist_id\":76849,\"revision\":\"1334161\"}"
    payload = "{\"artist_id\":" + str(id) + ",\"revision\":\"1334161\"}"

    response = requests.request("POST", url, data=payload, headers=headers)

    # print response.text
    responseJson = json.loads(response.text)
    allSubResponses.append(responseJson)


def searchAndFollow(artistName):
    artistIds = search(artistName)
    for id in artistIds:
        # print "sub one " + str(id)
        
        sub(id)

def readFileAndSearchAndFollow(fileInput):
    with open(fileInput, 'r') as fp:
        line = fp.readline()
        time.sleep(random.randint(1,6))
        while line:
            print line
            searchAndFollow(line.strip())
            line = fp.readline()


# search('Dj Tennis')

s = sys.argv[1]
# searchAndFollow(s)
readFileAndSearchAndFollow(s)

print allSubResponses

allSubResponses = None