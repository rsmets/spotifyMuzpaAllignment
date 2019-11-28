import requests, json

headers = {
    'Cookie': "SESS=6fb6428329bddc27c87f31871270f6c715bc53",
    'User-Agent': "PostmanRuntime/7.16.3",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "srv.muzpa.com",
    'Accept-Encoding': "gzip, deflate",
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
    print '\n\n\n'
    
    lowCount = 1000
    artistIds = []

    albums = responseJson['albums']
    for album in albums:
        tracks = album['tracks']
        for track in tracks:
            # if artistName in track['filename']:
            # print track['filename']
            if matchArtist(track['filename'], "Dj Tennis") > -1:
                print track['filename']
                artistsOnTracks = track['artists_ids']
                al = len(artistsOnTracks)
                print al
                if al < lowCount:
                    artistIds = artistsOnTracks
    
    print artistIds


def matchArtist(search, input):
    hit = search.lower().find(input.lower())
    print hit
    return hit

search('Dj Tennis')