rem pyinstaller està en el %PATH%
rem Cal haver generat FSincro.py a partir de FSincro.ui
rem -w fa que no es creï una consola quan s'executi
rem Els dos --add-data copien el text de l'ajuda i la icona a la carpeta de l'executable
rem --noconfirm fa que no es demani una confirmació de sobreescriptura a mig fer,
rem així el pyinstaller només para al final
rem Recordar que l'executable es troba a la carpeta dist

pyinstaller EditorKML_v2_2.py FinPpal.py Rutes.py FinestraRutes.py Ajuda.py Display.py -w --noconfirm --add-data PlantillaDoc.kml;. --add-data PlantillaRuta.kml;. --add-data Editor1.ico;. --add-data Ajuda.html;.

