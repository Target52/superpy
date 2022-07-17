[![Winc](https://global-uploads.webflow.com/5ee34869dd28cd4237e2a5f2/5f030fe26dc9fc19df8dc16a_Winc-logo-objects.svg)](https://www.wincacademy.nl/)





# Superpy
## _Supermarket command line tool_
<br/><br/>

##  Gebruikshandleiding



Zorg dat u in de Superpy folder bent om Superpy te gebruiken
```sh
cd superpy
```
Hier kunt u met de beschikbare commandos het systeem bedienen
```sh
python main.py advance-time 5
```


<br/><br/>
Superpy werk met de volgende commandos:

### advance-time
Met advance-time kunt u de huidige datum instellen<br>
Opties:<br>--help<br>
        --x (waarbij x een integer is), de datum neemt toe of af met x dagen (verplicht)
```sh
python main.py advance-time 5
```

### buy
Met buy koopt u producten<br>
opties:<br>--help<br>
        --product-name (verplicht)<br>
        --price (verplicht)<br>
        --expiration-date (verplicht)<br>
```sh
python main.py buy --product-name apple --price 2.1 --expiration-date 2022-12-03
```


### sell
Met sell verkoopt producten<br>
opties:<br>--help<br>
        --product-name (verplicht)<br>
        --price (verplicht)<br>
```sh
python main.py sell --product-name apple --price 3.1
```


### report inventory
Met inventory geeft u de voorraad weer<br>
opties:<br>--help<br>
        --today (inventory van vandaag)<br>
        --yesterday (inventory van gister)<br>
        --date (inventory van bepaalde datum)<br>
        --pdf (slaat de inventory op als PDF)
```sh
python main.py report inventory --date 2022-12-03 --pdf
```

### report revenue
Met revenue geeft u de omzet weer<br>
opties:<br>--help<br>
        --today (revenue van vandaag)<br>
        --yesterday (revenue van gister)<br>
        --date (revenue van bepaalde datum)<br>
```sh
python main.py report revenue --today
```

### report profit
Met profit geeft u de winst weer<br>
opties:<br>--help<br>
        --today (profit van vandaag)<br>
        --yesterday (profit van gister)<br>
        --date (profit van bepaalde datum)<br>
```sh
python main.py report profit --yesterday
```







