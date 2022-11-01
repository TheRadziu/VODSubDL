# VODSubDL
## Info
Skrypt oryginalnie służył do ściągania napisów z serwisu TVP VOD. Z czasem rozwinąłem go o funkcjonalność pobierania video.  
Abonament ABO jest wspierany.

## Abonament ABO (cookies)
TODO

## Ustawienia
`subtitleedit = "E:\subtitle edit\SubtitleEdit.exe"` - PATH do programu Subtitle edit (patrz: poniżej)  
`IDM = "C:\Program Files (x86)\Internet Download Manager\IDMan.exe"` - PATH do Internet Download Managera, jeśli uzywasz innej aplikacji patrz notki niżej  
`output_dir = r"E:\Downloads"` - PATH do folderu do którego mają zostać zapisane video i/lub napisy  
`DLSubs = True` - Czy pobierać napisy (domyślnie włączone)  
`DLVideo = True` - Czy pobierać video (domyślnie włączone)  
`Rozdzielczosc = "1080p"` - Rozdzielczość jaka ma zostać pobrana, dostępne rozdzielczości to: 2160p, 1080p, 720p, 544p, 450p  

## Zewnętrzne aplikacje
Internet Download Manager (Płatny, Darmowy Trial) - https://www.internetdownloadmanager.com/  
Subtitle Edit (Darmowy, Open Source) - https://github.com/SubtitleEdit/subtitleedit

## Limity i znane błędy
- Brak wsparcia dla DRM (materiały od BBC). Ta funkcja raczej nie będzie przeze mnie dodana.  
- BUG: Ustawienie rozdzielczości wyższej niż maksymalnie dostępna spowoduje wygenerowanie nieprawidłowego URL. (funkcja decide_resolution)

## Notki
1. Jeśli uzywasz innej aplikacji do pobierania plików edytuj linijkę na syntax odpowiadający twojej aplikacji;    
`subprocess.call([IDM, '/d', mp4_DL, '/p', output_dir, '/f', nazwa_pliku+'.mp4', '/n'])`  
gdzie: `IDM` - patrz Ustwienia, `mp4_DL` - URL do pliku, `output_dir` - patrz Ustawienia, `nazwa_pliku` - Nazwa pliku bez rozszerzenia
