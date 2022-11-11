## VODSubDL.py v2.31
## Napisane w Python 3.9 przez TheRadziu
# TODO:
# - Dodać poprawną detekcję i reakcję na "ERROR: Przekroczono limit jednoczesnych odtworzeń"

### Ustawienia ###
subtitleedit = "E:\subtitle edit\SubtitleEdit.exe"
IDM = "C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
output_dir = r"E:\Downloads"
drzewko_folderowe = True
DLSubs = True
DLVideo = True
max_rozdzielczosc = "2160p"
spiulkolot = 5
## DRM STUFF ##
ytdlp = r"E:\Downloads\VODSubDL\yt-dlp.exe"
mp4decr = r"E:\Downloads\VODSubDL\mp4decrypt.exe"
ffmpeg_bin = r"E:\Programy\FFMPEG\ffmpeg.exe"
downey = r"E:\Downloads\VODSubDL\downey.exe"
### koniec ustawień ###

import os
import json
import requests
import urllib.request
import subprocess
import re
import http.client
import errno
import time
import base64
import sys
import xmltodict
from cpix.drm import widevine
from unidecode import unidecode

def parseCookieFile(cookiefile):
    cookies = {}
    with open (cookiefile, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                lineFields = re.findall(r'[^\s]+', line)
                try:
                    cookies[lineFields[5]] = lineFields[6]
                except Exception as e:
                    pass
    return cookies

def parse_mpd(mpd_url):
    r = requests.get(url=mpd_url)
    r.raise_for_status()
    xml = xmltodict.parse(r.text)
    mpd = json.loads(json.dumps(xml))
    tracks = mpd['MPD']['Period']['AdaptationSet']
    for video_tracks in tracks:
        if video_tracks['@mimeType'] == 'video/mp4':
            wysokosc = video_tracks['@maxHeight']
            for t in video_tracks["ContentProtection"]:
                if t['@schemeIdUri'].lower() == "urn:mpeg:dash:mp4protection:2011":
                    kid = t["@cenc:default_KID"]
    return kid, wysokosc

def get_real_id(url):
    real_api_response = requests.get('https://vod.tvp.pl/api/products/vods/'+url[-6:]+'?lang=pl&platform=BROWSER')
    real_api_json = json.loads(real_api_response.text)
    real_id = real_api_json['externalUid']
    return real_id

def check_url(url):
    urlC = http.client.HTTPConnection(url.split("/", 3)[2])
    urlC.request("HEAD", "/"+url.split("/", 3)[3])
    return urlC.getresponse().status

def decide_resolution(url, Rozdzielczosc):
    tabela_rozdzielczosci = {
    "2160p" : "11",
    "1080p" : "9",
    "720p" : "7",
    "544p" : "6",
    "450p" : "5",
    }
    urlA = re.match(r"(.*)-(.*).mp4", url)
    if Rozdzielczosc not in tabela_rozdzielczosci:
        print("\nOSTRZEŻENIE! Zdefiniowano złą maksymalną rozdzielczość! Wideo zostanie pobrane w najlepszej dostępnej jakości!\nZnaleziono rozdzielczość: ", end = '')
        Rozdzielczosc = "2160p"
    urlB = urlA[1]+"-"+tabela_rozdzielczosci[Rozdzielczosc]+".mp4"
    for i, (k, v) in enumerate(tabela_rozdzielczosci.items()):
        if i >= list(tabela_rozdzielczosci.keys()).index(Rozdzielczosc):
          urlB = urlA[1]+"-"+v+".mp4"
          if check_url(urlB) == 200:
            print(" ["+k+"]")
            break
    return urlB
    
def single_vid_api(id):
    vod_url = 'https://vod.tvp.pl/sess/TVPlayer2/api.php?id='+id+'&@method=getTvpConfig&@callback=callback'
    response = requests.get(vod_url, cookies=ciastka)
    startidx = response.text.find('(')
    endidx = response.text.rfind(')')
    return json.loads(response.text[startidx + 1:endidx])

def batch_season_api(id):
    season_api_response = requests.get('https://vod.tvp.pl/api/products/vods/serials/'+id[-6:]+'/seasons?lang=pl&platform=BROWSER')
    season_api_json = json.loads(season_api_response.text)
    season_dict = {}
    season_range = range(0, len(season_api_json))
    for n in season_range:
        season_dict[season_api_json[n]['title']] = season_api_json[n]['id']
    return season_dict
    
def get_episode_ids(id, seasonid):
    whole_season_response = requests.get('https://vod.tvp.pl/api/products/vods/serials/'+id[-6:]+'/seasons/'+str(seasonid)+'/episodes?lang=pl&platform=BROWSER')
    whole_season_json = json.loads(whole_season_response.text)
    real_id_list = []
    id_range = range(0, len(whole_season_json))
    for n in id_range:
        real_id_list.append(whole_season_json[n]['externalUid'])
    return real_id_list

def name_and_dir(url, output_dir, batch):
    if batch == True:
        url = 'odcinek'
    output_dir_set = None
    tytul = re.sub('[^a-zA-zżźćńółęąśŻŹĆĄŚĘŁÓŃ0-9 \n\.]', '', api_response['content']['info']['title']).lstrip()
    sezon = re.sub('[^0-9]', '', api_response['content']['info']['season'])
    if 'odcinek' in url:
        if sezon is None or len(sezon) == 0 or len(sezon) > 3:
            nazwa_pliku = (tytul+" odc. "+f"{api_response['content']['info']['episode']:02d}")
        else:
            nazwa_pliku = (tytul+" S"+f"{int(sezon):02d}"+"E"+f"{api_response['content']['info']['episode']:02d}")
    else:
        nazwa_pliku = tytul
    if output_dir_set is None:
        output_dir_set = output_dir
    if drzewko_folderowe and 'odcinek' in url:
        if sezon is None or len(sezon) == 0 or len(sezon) > 3:
            output_dir = output_dir_set+"\\"+tytul+"\\Sezon nieznany"
        else:
            output_dir = output_dir_set+"\\"+tytul+"\\Sezon "+sezon
    elif drzewko_folderowe and 'filmy' in url:
        output_dir = output_dir_set+"\\"+tytul
    return nazwa_pliku, output_dir

def download_video(api_response, names):
    output_dir = names[1]
    nazwa_pliku = unidecode(names[0])
    if api_response['content']['files'][0]['protection']:
        for wynik in api_response['content']['files']:
            if wynik['url'].endswith('.ism'):
                mpd = wynik['url']+'?indexMode'
                license_url = wynik['protection']['licenseServers'][2]['url']
                rozdzielczosc = parse_mpd(wynik['url'])[1]
                print(' ['+rozdzielczosc+'p] [DRM]')
                try:
                    subprocess.call([ytdlp, '--quiet', '--no-warnings', '--progress', '-N', '16', '--output', nazwa_pliku+'.mp4', '--allow-u', mpd])
                    print('Pomyślnie pobrano odcinek.')
                except:
                    print('BŁĄD! Pobieranie odcinka nie powiodło się!')
                try:
                    pssh_enc = widevine.generate_pssh(
                        [parse_mpd(mpd)[0]],
                        None,
                        None,
                        0,
                        None
                    )
                    pssh_bin_1 = str(base64.b64encode(pssh_enc), "ascii")
                    print('!!!--------!!!')
                    print('MPD URL: '+mpd)
                    print('PSSH: '+pssh_bin_1)
                    print('License URL: '+wynik['protection']['licenseServers'][2]['url'])
                    print('!!!--------!!!')
                except KeyboardInterrupt:
                    print('Anulowano!')
                    break
                except Exception as e:
                    print(e)
                    break
                try:
                    #yt-dlp jest głupie a my nie
                    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
                        for plik in files:
                            if plik.startswith(nazwa_pliku) and plik.endswith(".mp4"):
                                plik_video = plik
                            elif plik.startswith(nazwa_pliku) and plik.endswith(".m4a"):
                                plik_audio = plik
                    deckey_raw = subprocess.check_output([downey, '--lic-server', license_url, '--pssh', pssh_bin_1])
                    deckey = re.findall(r"\w{32}:\w{32}", deckey_raw.decode('utf-8'))
                    subprocess.call([mp4decr, '--key', deckey[0], plik_video, nazwa_pliku+'.decrypted.mp4'])
                    subprocess.call([mp4decr, '--key', deckey[0], plik_audio, nazwa_pliku+'.decrypted.m4a'])
                    subprocess.call([ffmpeg_bin, '-hide_banner', '-v', 'fatal', '-nostats', '-i', nazwa_pliku+'.decrypted.mp4', '-i', nazwa_pliku+'.decrypted.m4a', '-vcodec', 'copy', '-acodec', 'copy', nazwa_pliku+'.mp4'])
                    os.remove(plik_video)
                    os.remove(plik_audio)
                    os.remove(nazwa_pliku+'.decrypted.mp4')
                    os.remove(nazwa_pliku+'.decrypted.m4a')
                    time.sleep(2)
                    os.replace(nazwa_pliku+'.mp4', output_dir+'/'+nazwa_pliku+'.mp4')
                    print('Pomyślnie rozszyfrowano materiał.')
                except Exception as e:
                    print('BŁĄD! Rozszyfrowywanie materiału nie powiodło się!')
                    print(e)
        pass
    else:
        for wynik in api_response['content']['files']:
            if wynik['url'].endswith('.mp4'):
                mp4_url = wynik['url']
                break
        mp4_DL = decide_resolution(mp4_url, max_rozdzielczosc)
        subprocess.call([IDM, '/d', mp4_DL, '/p', output_dir, '/f', nazwa_pliku+'.mp4', '/n'])
        print("Rozpoczęto pobieranie wideo za pomocą IDM")
    print("---------")

def download_and_convert_subs(url, names):
    output_dir = names[1]
    nazwa_pliku = unidecode(names[0])
    subs = re.match(r".*'url': '//(.*).xml'", str(api_response['content']['subtitles']))
    try:
        urllib.request.urlretrieve('http://'+subs[1]+'.xml', nazwa_pliku+'.xml')
        print("Pobrano napisy XML")
        subprocess.run([subtitleedit, "/convert", nazwa_pliku+'.xml', "srt", "/outputfolder:"+output_dir], stdout=subprocess.DEVNULL)
        os.remove(nazwa_pliku+".xml")
        print("Zapisano napisy jako .SRT i usunięto .XML")
    except:
        print("Wystąpił błąd pobierania napisów - prawdopodobnie nie istnieją")
    print("---------")

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else: raise

if DLSubs or DLVideo:
    output_dir_set = None
    api_response = None
    if os.path.isfile('tvp.pl_cookies.txt'):
        print("Poprawnie wykryto plik z ciasteczkami TVP")
        ciastka = parseCookieFile('tvp.pl_cookies.txt')
    else:
        print("Nie wykryto ciasteczek TVP. Ściąganie plików ABO zakończy się błędem!")
        ciastka = None
while True:
    url = input('Podaj URL do odcinka lub filmu: ')
    if not 'vod.tvp.pl' in url:
        print('BŁĄD! Podano nieprawidłowy URL!')
        continue
    if 'odcinek' in url or 'filmy' in url:
        try:
            api_response = single_vid_api(get_real_id(url))
        except:
            print("BŁĄD! Nie masz dostępu do tego materiału! (sprawdź abonament ABO lub czy masz wykupiony dostęp!)")
            continue
        mkdir_p(name_and_dir(url, output_dir, False)[1])
        print("Wybrano: "+name_and_dir(url, output_dir, False)[0], end = '')
    elif 'odcinki' in url:
        lista_sezonow = batch_season_api(url)
        print('Znaleziono '+str(len(lista_sezonow))+' sezon/ów!')
        wybor = input('Wybierz numer sezonu (1-'+str(len(lista_sezonow))+') lub wybierz 0 dla wszystkich dostepnych sezonów: ')
        while not wybor.isdigit() or int(wybor) > len(lista_sezonow):
            wybor = input('BŁĄD! Zły wybór! Można tylko wybrać cyfrę od 0 do '+str(len(lista_sezonow))+'! Spróbuj ponownie!: ')
        wybor = int(wybor)
        if wybor == 0:
            print('wybrano wszystkie dostępne sezony!')
            for i, (k, v) in enumerate(lista_sezonow.items()):
                num = 0
                for real_id_episode in get_episode_ids(url, v):
                    api_response = single_vid_api(real_id_episode)
                    num +=1
                    print("Wybrano: "+name_and_dir(url, output_dir, True)[0]+" ("+str(num)+"/"+str(len(get_episode_ids(url, v)))+")", end = '')
                    mkdir_p(name_and_dir(url, output_dir, True)[1])
                    if DLVideo:
                        download_video(api_response, name_and_dir(url, output_dir, True))
                    if DLVideo is False:
                        print(" [Napisy]")
                    if DLSubs:
                        download_and_convert_subs(url, name_and_dir(url, output_dir, True))
                    time.sleep(spiulkolot)
            break
        else:
            for i, (k, v) in enumerate(lista_sezonow.items()):
                if i == wybor+-1:
                    num = 0
                    for real_id_episode in get_episode_ids(url, v):
                        api_response = single_vid_api(real_id_episode)
                        num +=1
                        print("Wybrano: "+name_and_dir(url, output_dir, True)[0]+" ("+str(num)+"/"+str(len(get_episode_ids(url, v)))+")", end = '')
                        mkdir_p(name_and_dir(url, output_dir, True)[1])
                        if DLVideo:
                            download_video(api_response, name_and_dir(url, output_dir, True))
                        if DLVideo is False:
                            print(" [Napisy]")
                        if DLSubs:
                            download_and_convert_subs(url, name_and_dir(url, output_dir, True))
                        time.sleep(spiulkolot)
            continue
        continue
    else:
        print('Ten typ materiału nie jest wspierany przez VODSubDL. Zgłoś to autorowi!')
    if DLVideo:
        download_video(api_response, name_and_dir(url, output_dir, False))
    if DLSubs:
        if DLVideo is False:
            print(" [Napisy]")
        download_and_convert_subs(url,name_and_dir(url, output_dir, False))
else:
    print('Funkcjonalnosc VODSubDL wyłączona. Włącz conajmniej jedną funkcję!')
