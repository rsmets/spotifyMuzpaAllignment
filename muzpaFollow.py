import requests, json, sys, time, random, os, errno

def search(artistName):
    url = "https://srv.muzpa.com/a/ms/media/search"

    querystring = {
        # "matchonly":"true"
        "mp3prefered":"false",
        "page":"0",
        "popular_order":"false",
        "text":artistName
    }

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
                    # print track['artist']
                    if matchString(track['artist'], artistName) > -1:
                        # print track['artist']
                        artistsOnTracks = track['artists_ids']
                        al = len(artistsOnTracks)
                        # print al
                        if al < lowCount:
                            artistIds = artistsOnTracks
        
    # print artistIds
    return artistIds

def trackSearch(trackName, artist):
    url = "https://srv.muzpa.com/a/ms/media/search"

    querystring = {
        "matchonly":"true",
        "mp3prefered":"false",
        "page":"0",
        "popular_order":"true",
        "text":trackName
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    time.sleep(random.randint(3,7))

    responseJson = json.loads(response.text)

    albums = responseJson['albums']
    if albums: 
        for album in albums:
            tracks = album['tracks']
            if tracks:
                for track in tracks:
                    title = track['title']
                    print title
                    # if matchString(title, trackName) > -1:
                    if matchString(track['artist'], artist) > -1:
                        print 'FOUND TRACK ARTIST ' + artist
                        t = track['title']
                        st = track['subtitle']

                        if st is not None:
                            print 'title ' + t + "subt " + st
                            t = t + " (" + st + ")"

                        return {
                            "id": track['id'], 
                            "title": t, 
                            "label": track['label']['nm'],
                            "format": track['format'],
                        }
        
    # print artistIds
    # return artistIds
    return False

# def searchTrackAndDownload(trackName, artistName):
def searchTrackAndDownload(trackInput, playlist, path):

    if 'Original Mix' in trackInput:
        trackInput = trackInput[:-15]
        print 'NEW TRACK INPUT ' + trackInput

    trackNameParts = trackInput.split(' ~ ')
    artistName = trackNameParts[0]
    trackName = trackNameParts[1]

    trackInfo = trackSearch(trackInput, artistName)
    if trackInfo != False:
        print 'trackInfo ' + str(trackInfo)
        
        trackId = trackInfo['id']
        trackLabel = trackInfo['label']
        format = trackInfo['format']
        trackTitle = trackInfo['title']
        # print trackLabel

        download(trackId, trackTitle, artistName, trackLabel, format, playlist, path)
    else:
        print 'NOPE'

def download(id, name, artist, label, format, playlist, path):

    print 'attempting download ' + str(id) + " name " + name
    url = "https://srv.muzpa.com/dwnld/track/" + str(id) + "." + format + "?iframe"

    # payload = "{\"artist_id\":" + str(id) + ",\"revision\":\"1334161\"}"

    # response = requests.request("POST", url, data=payload, headers=headers)
    response = requests.request("GET", url, headers=headers, params=())

    
    if label is not None:
        finalPath = path + '/' + artist + ' - ' + name + ' [' + label + '].' + format
        print 'Downloading to: ' + finalPath
        open(finalPath, 'wb').write(response.content)
    else:
        finalPath = path + '/' + artist + ' - ' + name + '.' + format
        print 'Downloading to: ' + finalPath
        open(finalPath, 'wb').write(response.content)

    # print response.text
    # responseJson = json.loads(response.text)
    # allSubResponses.append(responseJson)

def matchString(search, input):
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

def readFileAndSearchAndDownload(fileInput):
    path = './music/' + fileInput
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
    with open(fileInput, 'r') as fp:
        line = fp.readline()
        time.sleep(random.randint(1,3))
        while line:
            print line
            searchTrackAndDownload(line.strip(), fileInput, path)
            line = fp.readline()


s = sys.argv[1]
# token = sys.argv[2]
token = "SESS=abe178d76ef28b30b4dbbdb2515973a3175970"

headers = {
    'Cookie': token,
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "srv.muzpa.com",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

# searchAndFollow(s)
# readFileAndSearchAndFollow(s)

# print allSubResponses

# allSubResponses = None

# searchTrackAndDownload('Oedipus Complex', 'K Nass')
# searchTrackAndDownload('Roberto Surace ~ Joys - Extended Mix')
# searchTrackAndDownload('6 AM - Original Mix', 'Sebastian Porter')
# searchTrackAndDownload('Sebastian Porter ~ 6 AM - Original Mix')

# readFileAndSearchAndDownload("playlists/t_cutz")
readFileAndSearchAndDownload(s)