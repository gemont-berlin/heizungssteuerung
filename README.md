# Heizungssteuerung

### Einrichtung

- stecke die SD-Karte des Pis in den Computer oder in einen SD-Karten Lesegerät
- die aktuelle RaspianOS-Version [herunterladen](https://www.raspberrypi.org/downloads/raspbian/)
- ISO auf SD-Karte brennen

  #### Windows
  
  - stecke die SD-Karte des Pis in den Computer oder in einen SD-Karten Lesegerät
  - wähle unter `Device` die SD-Karte des Pis aus
  - klicke auf das Ordersymbol, um das heruntergeladene Image auszuwählen
  - klicke auf `Write`, damit das Image auf die SD-Karte des Pis geschrieben wird
  ![alt](https://fusix.de/upload/win32diskimager.png "Win32DiskImager")

  #### Mac
  
  - wähle im rechten Bereich der Anwendung die SD-Karte des Pis aus
  - klicke auf `...`, um das heruntergeladene Image auszuwählen
  - klicke auf `Restore Backup`, damit das Image auf die SD-Karte des Pis geschrieben wird
  ![alt text](https://fusix.de/upload/apibaker.png "Apple Pi Baker")
  
  #### Linux
  
  - führe `df -h` aus, um zu sehen welche Datenträger eingehängt sind
  - stecke nun die SD-Karte des Pis in den Computer oder in einen SD-Karten Lesegerät
  - führe `df -h` erneut aus
  - der neu aufgeführte Datenträger ist die SD-Karte (z.B. `/dev/mmcblk0p1` oder `/dev/sdd1`)
  -  `p1` oder `1` mit `p0`beziehungsweise `0` ersetzen, damit auf die gesamte SD-Karte geschrieben wird und nicht nur auf eine Partition
  - damit auf die SD-Karte geschrieben werden kann muss diese ausgehängt werden mit z.B. `umount /dev/mmcblk0p0` (Bei mehreren Partitionen alle aushängen)
  - zum schreiben verwende `dd bs=4M if=2016-03-18-raspbian-jessie.img of=/dev/mmcblk0p0`
  
- Abhängigkeiten installieren: `sudo apt-get install python-mysqldb`
- in /root/heizung.py die Variable room auf die Raumnummer setzen.
- Fallbackwerte für Start- und Endzeit der Tages festlegen, damit die Solltemperatur gesetzt werden kann.
- Solltemperatur festlegen (fallback)
- MySQL-Verbindungsdaten abändern auf Server IP und Benutzernamen mit Passwort angeben
  - auf Server localhost als IP verwenden

---

### Einrichtung Server

- Vorgehensweise wie oben
- Apache installieren
  - `sudo apt-get install apache2`
- php installieren
  - `sudo apt-get install php5`
- mysql-server installieren
  - `sudo apt-get install mysql-server mysql-client php5-mysql`
  - root User Passwort festlegen
  - root User Passwort bestätigen
- phpMyAdmin installieren
  - `sudo apt-get install php5-mysql phpmyadmin`
  - `apache2` auswählen
  - das System benötigt einige Datenbanken, deshalb mit `yes` bestätigen
  - das root User Passwort des MySQL-Servers angeben
  - root User Passwort für phpMyAdmin festlegen
  - Passwort bestätigen
  - falls phpMyAdmin nicht erreichbar ist über `http://<IP>/phpmyadmin`
    - ln -s /etc/phpmyadmin/apache.conf /etc/apache2/conf.d/phpmyadmin.conf
- über phpmyadmin Zugriff von Außen erlauben
  - auf die Schaltfläcge `Benutzer` klicken
  - für den jeweiligen User den Host auf `localhost, %` setzen
- in /etc/mysql/my.cnf `bind-adress` auskommentieren (Editor: `sudo nano /etc/mysql/my.cnf`)

---

### Starten des Skriptes

`sudo python /root/heizung.py 1` ==> steuert Heizungen an den GPIO Pins 23, 25, 27
    
`sudo python /root/heizung.py 2`==> steuert Heizungen an den GPIO Pins 17, 22, 24
