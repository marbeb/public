NAPALM AND NETMIKO


pobiera interfaces i wrzuca do zagniezdzonej dictionary,
pobiera tylko i wylacznie key (czyli nasz interface) i dodaje to do listy

!!!! USUWA INTERFACE VLAN I ZOSTAWIA SAME FIZYCZNE INTERFACE

1. Na poczatku tworzy backup calej konfiguracji
2. sprawdza w jakim vlanie jest kazdy interface
3. sprawdza czy na danym porcie nie bylo czasami 'auth open' (w wyjatkowych sytuacjach jest to konieczne)
4. defaultuje i wrzuca cala tabele komend ktore powinny byc w danym vlanie
5. jezeli wczesniej dany port mial ustawione 'auth open' to po dodaniu tabeli komend dodaje jeszcze 'auth open' do danego portu
6. porty skonfigurowane sa wedlug konkretnego standardu (z wyjatkami, patrz punkt 5.)

7. Na koncu pokazuje statystyki:
  - status portu przed oraz po zmianie,
  

DODAC
1. zapisac status autentykacji przed oraz po zmianie - na końcu wyswietlic porównanie