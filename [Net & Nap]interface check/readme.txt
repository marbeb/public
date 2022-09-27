NAPALM AND NETMIKO


pobiera interfaces i wrzuca do zagniezdzonej dictionary,
pobiera tylko i wylacznie key (czyli nasz interface) i dodaje to do listy

!!!! USUWA INTERFACE VLAN I ZOSTAWIA SAME FIZYCZNE INTERFACE

1. Na poczatku tworzy backup calej konfiguracji (zrobic jeszcze)
2. sprawdza w jakim vlanie jest kazdy interface
3. sprawdza czy na danym porcie nie bylo czasami 'auth open'
4. defaultuje i wrzuca cala tabele komend ktore powinny byc w danym vlanie
5. jezeli wczesniej dany port mial ustawione 'auth open' to po dodaniu tabeli komend dodaje jeszcze 'auth open' do danego portu
6. Porty skonfigurowane sa wedlug standardu (z wyjatkami, patrz punkt 5.)

7. Na koncu pokazuje statystyki czyli czy dany port byl up przed zmiana i status po zmianie

POMYSLY
1. ZAPISAC STATUS PORTU PRZED ZMIANA CONF status nac oraz porównać ze statusem po zakonczeniu calego skryptu