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

## Zewnętrzne aplikacje
Internet Download Manager (Płatny, Darmowy Trial) - https://www.internetdownloadmanager.com/  
Subtitle Edit (Darmowy, Open Source) - https://github.com/SubtitleEdit/subtitleedit

## Limity i znane błędy
- Brak wsparcia dla DRM (materiały od BBC). Ta funkcja raczej nie będzie przeze mnie dodana.  
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
