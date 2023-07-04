Program laczy sie do Netboxa wykorzystujac API,
pobiera liste fizycznych sprzetow ktore maja przypisany tag 'backup'
Sprawdza taki kazdy sprzet i zapisuje adres IP (obrabia go aby usunac maske) oraz custom field 'netmiko module'
gdzie zapisane sa jakiego modulu ma uzyc.

Sprawdza jakie pliki zostaly znalezione na dysku
Wysyla maila z informacjami jakie zebral:
- do ktorych urzadzen sie podlaczyl
- do jakich nie i z jakiego powodu
- ile plikow conf sie utworzylo
- ile sie nie utworzylo
- czas trwania programu