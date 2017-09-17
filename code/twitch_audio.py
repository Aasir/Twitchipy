import requests, json, streamlink, time, sys, json, Keys
import recognizer as Recognizer

streamFile = "temp.mp4"

def getTwitchStream(user):
    stream = streamlink.streams("http://twitch.tv/" + user)
    #print(stream.keys())

    # Check to see if stream is live
    if bool(stream) is False:
        result = {'channelExists' : False}
        print("Stream is not live!")
        return result

    stream = stream['audio_only']
    fd = stream.open()
    start_time_in_seconds = time.time()
    time_limit = 5
    with open(streamFile , 'wb') as f:
        while time.time() - start_time_in_seconds < time_limit:
            data = fd.read(1024)
            f.write(data)
    f.close()

    result = {'channelExists' : True}
    return result

def getSongID():
    config = {
        'host':Keys.ACR_HOST,
        'access_key':Keys.ACR_ACCESS_KEY,
        'access_secret':Keys.ACR_SECRET_KEY,
        'timeout':5
    }

    re = Recognizer.ACRCloudRecognizer(config)
    buf = open(streamFile, 'rb').read()

    Recognizer.acrcloud_extr_tool.set_debug()
    music_info = json.loads(re.recognize_by_filebuffer(buf, 10))

    if music_info['status']['msg'] != 'Success':
        result = {
        'songFound' : False
        }
        return result

    #print(music_info)
    track_info = music_info['metadata']['music']
    #print(track_info[0])

    result = {
    'songFound' : True,
    'Artist' : track_info[0]['artists'][0]['name'],
    'Title' : track_info[0]['title'],
    'Album' : track_info[0]['album']['name'],
    'Spotify' : track_info[0]['external_metadata']['spotify']
    }

    return result
