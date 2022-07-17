[![Winc](https://global-uploads.webflow.com/5ee34869dd28cd4237e2a5f2/5f030fe26dc9fc19df8dc16a_Winc-logo-objects.svg)](https://www.wincacademy.nl/)





# Superpy
## _Supermarket command line tool_
<br/><br/>


Superpy is een command line tool welke gebruikt kan worden voor het bijhouden van een supermarkt inventaris.

ik heb de opdracht eenvoudig gehouden, tijdens mijn leerweg heb ik ontdekt dat front end dev mijn voorkeur geniet. het back end gedeelte wil ik wel graag afmaken maar ik heb niet heel veel tijd over dus vandaar de eenvoudige opzet.


Argparse is gebruikt voor de command line interactie. De gegevens worden uit csv files gehaald en ook weer weggeschreven. De weergave heb ik opgeleukt mer Rich, waardoor er wat kleur en tabellen kunnen worden gebruikt. De report inventory functie heeft een filter om de niet meer houdbare artikelen eruit te halen zodat die niet in de inventory verschijnen. Als optie kan het inventory report ook als PDF worden weggeschreven. Hiet heb ik reportlab voor gebruikt.
```sh
python main.py report inventory --date 2022-12-03 --pdf
```

Een probleem waar ik tegenaan liep was dat zowel rich als reportlab de klasse Table importeren hierdoor kreeg ik een foutmelding bij de tweede call naar Table. Het heeft wat tijd gekost voordat ik er achter kwam maar ik heb het uiteindelijk opgelost door de Table van reportlan onder een andere naam te importeren
```sh
from reportlab.platypus import SimpleDocTemplate, Table as Table2, TableStyle
```