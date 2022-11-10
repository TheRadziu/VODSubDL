# VODSubDL
## Info
Skrypt oryginalnie służył do ściągania napisów z serwisu TVP VOD. Z czasem rozwinąłem go o funkcjonalność pobierania video.  
Abonament ABO jest wspierany.

## Abonament ABO (cookies)
1. Zainstaluj dodatek "Get cookies.txt" - https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid  
2. Wejdź na strone TVP VOD i się zaloguj. Upewnij się że masz aktywny abonament ABO.  
3. W "Get cookies.txt" upewnij się że `Get cookies.txt for vod.tvp.pl` jest wyświetlane u góry, po czym kliknij Export poniżej. Zapisz plik `tvp.pl_cookies.txt` w lokacji z VODSubDL.py.  
4. Gotowe. Przy uruchomieniu skryptu zostanie wyświetlony komunikat czy ciasteczka zostały załadowane poprawnie.

## Ustawienia
`subtitleedit = "E:\subtitle edit\SubtitleEdit.exe"` - PATH do programu Subtitle edit (patrz: poniżej)  
`IDM = "C:\Program Files (x86)\Internet Download Manager\IDMan.exe"` - PATH do Internet Download Managera, jeśli uzywasz innej aplikacji patrz notka 1 niżej  
`output_dir = r"E:\Downloads"` - PATH do folderu do którego mają zostać zapisane video i/lub napisy  
`drzewko_folderowe = True` - Generuje podfoldery `Tytuł\Sezon X\`  
`DLSubs = True` - Czy pobierać napisy (domyślnie włączone)  
`DLVideo = True` - Czy pobierać video (domyślnie włączone)  
`max_rozdzielczosc = "2160p"` - Maksymalna rozdzielczość jaka ma zostać pobrana, dostępne wartości to: 2160p, 1080p, 720p, 544p, 450p.  
Dokładniejsze wyjasnienie działania ustawienia `max_rozdzielczosc` w notce 2 niżej.  
`spiulkolot = 5` - W trybie całej serii, czas w sekundach jaki ma skrypt odczekać przed rozpoczęciem pobierania kolejnego odcinka.  
**DRM**  
 Wszystkie czynności związane z obsługą materiałów DRM wymagają prawidłowo skonfigurowanego(headers.py + WŁASNE działające CDM) i lekko zmodyfikowanego skryptu WSK-KEY (wykomentowanie kilku linijek w l3.py).  
`ytdlp = r"E:\Downloads\VODSubDL\yt-dlp.exe"` - PATH do programu yt-dlp (patrz: poniżej)  
`mp4decr = r"E:\Downloads\VODSubDL\mp4decrypt.exe"` - PATH do programu mp4decrypt (patrz: niżej)  
`ffmpeg_bin = r"E:\Programy\FFMPEG\ffmpeg.exe"` - PATH do programu ffmpeg (patrz:niżej)  
`wkskey = r"E:\Downloads\VODSubDL\keys"`- PATH do skryptu wsk-key (patrz: niżej)  

## Zewnętrzne aplikacje
Internet Download Manager (Płatny, Darmowy Trial) - https://www.internetdownloadmanager.com/  
Subtitle Edit (Darmowy, Open Source) - https://github.com/SubtitleEdit/subtitleedit  
yt-dlp (Darmowy, Open Source) - https://github.com/yt-dlp/yt-dlp  
mp4decrypt (Darmowy) - https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-639.x86_64-microsoft-win32.zip  
ffmpeg (Darmowy, Open Source) - https://ffmpeg.org/download.html  
wks-key (Darmowy, Open Source) - https://github.com/weapon121/WKS-KEY  

## Limity i znane błędy
- Wsparcie dla DRM istnieje, ale wszystkie issues związane z pomocą jak używać będą zamykane bez odpowiedzi.  
- BUG: Przy jednoczesnym pobieraniu 3 materiałów ABO na raz, przy próbie pobrania czwartego skrypt błędnie zareaguje tak jakby abonament ABO nie był dostępny (Powód: "ERROR: Przekroczono limit jednoczesnych odtworzeń")  

## Planowane zmiany:
- Poprawa bugów wspomnianych wyżej.  

## Notki
1. Jeśli uzywasz innej aplikacji do pobierania plików edytuj linijkę na syntax odpowiadający twojej aplikacji;    
`subprocess.call([IDM, '/d', mp4_DL, '/p', output_dir, '/f', nazwa_pliku+'.mp4', '/n'])`  
gdzie: `IDM` - patrz Ustawienia, `mp4_DL` - URL do pliku, `output_dir` - patrz Ustawienia, `nazwa_pliku` - Nazwa pliku bez rozszerzenia  
2. W przypadku braku dostępności wideo w tej rozdzielczości zostanie pobrana najwyższa dostępna jakość na przykład:  
\[LEGENDA: ustawiona max_rozdzielczosc -> pobrana najlepsza rozdzielczość]  
2160p -> 1080p  
2160p -> 544p  
1080p -> 544p  
720p -> 544p  
