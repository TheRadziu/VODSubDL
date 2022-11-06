## VODSubDL.py v2.27
## Napisane w Python 3.9 przez TheRadziu
# TODO:
# - Dodać poprawną detekcję i reakcję na "ERROR: Przekroczono limit jednoczesnych odtworzeń"

### Settings ###
subtitleedit = "E:\subtitle edit\SubtitleEdit.exe"
IDM = "C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
output_dir = r"E:\Downloads"
DLSubs = True
DLVideo = True
max_rozdzielczosc = "2160p"
### end of Settings ###

import os
import json
import requests
import urllib.request
import subprocess
import re
import http.client

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

if DLSubs or DLVideo:
        if os.path.isfile('tvp.pl_cookies.txt'):
            print("Poprawnie wykryto plik z ciasteczkami TVP")
            ciastka = parseCookieFile('tvp.pl_cookies.txt')
        else:
            print("Nie wykryto ciasteczek TVP. Ściąganie plików ABO zakończy się błędem!")
            ciastka = None
while True:
    url = input('Podaj URL do odcinka: ')
    if 'odcinek' in url:
        vod_url = 'https://vod.tvp.pl/sess/TVPlayer2/api.php?id='+get_real_id(url)+'&@method=getTvpConfig&@callback=callback'
        try: 
            response = requests.get(vod_url, cookies=ciastka)
            startidx = response.text.find('(')
            endidx = response.text.rfind(')')
            data = json.loads(response.text[startidx + 1:endidx])
        except:
            print("BŁĄD! Materiały ABO wymagają ciasteczka z ważnym abonamentem ABO!")
            continue
        nazwa_pliku = (data['content']['info']['title']+' odc. '+str(data['content']['info']['episode']))
        print("Wybrano: "+nazwa_pliku, end = '')
        if DLVideo:
            if data['content']['files'][0]['protection']:
                print(' [DRM]\nBŁĄD! Wsparcie dla DRM (Playready, fairplay, widevine) nie jest dostępne.')
                print('Klucz DRM dla odcinka: '+data['content']['files'][0]['protection']['key'])
            else:
                for wynik in data['content']['files']:
                    if wynik['url'].endswith('.mp4'):
                        mp4_url = wynik['url']
                        break
                mp4_DL = decide_resolution(mp4_url, max_rozdzielczosc)
                subprocess.call([IDM, '/d', mp4_DL, '/p', output_dir, '/f', nazwa_pliku+'.mp4', '/n'])
                print("Rozpoczęto pobieranie odcinka za pomocą IDM")
        if DLSubs:
            subs = re.match(r".*'url': '//(.*).xml'", str(data['content']['subtitles']))
            if DLVideo is False:
                print(" [Napisy]")
            try:
                urllib.request.urlretrieve('http://'+subs[1]+'.xml', nazwa_pliku+'.xml')
                print("Pobrano napisy XML")
                subprocess.run([subtitleedit, "/convert", nazwa_pliku+'.xml', "srt", "/outputfolder:"+output_dir], stdout=subprocess.DEVNULL)
                os.remove(nazwa_pliku+".xml")
                print("Zapisano napisy jako .SRT i usunięto .XML")
            except:
                print("Wystąpił błąd pobierania napisów - prawdopodobnie nie istnieją")
        print("---------")
    else:
        print('BŁAD! Wymagany link do odcinka, nie do listy odcinków!')
else:
    print('Funkcjonalnosc VODSubDL wyłączona. Włącz conajmniej jedną funkcję!')
