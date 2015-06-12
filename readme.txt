Vorgehen bei einer ADW Messung.

1. Vor der Messung
   - ADW - Ablüftung anschalten
   - Linseis Messerfassung einschalten
   - CO-Detektor kontrollieren (Gerät läuft immer!)

2. Probenvorbereitung
   - Korbgröße auswählen
   - Probe einwiegen (Gewicht / TL Nummer notieren)
   - Probe in den ADW-Ofen stellen (OFEN NICHT ANSCHALTEN)

3. Messerfassung (Stand 11.06.2015)
   - Rechner starten (PI)
   - Auf der Oberfläche home/TLXXXX_Blanko Ordner suchen und kopieren
   - Dem kopierten Ordner einen neuen Namen geben mit der passenden TL Nummer
   - Datei Vorlage.py mit einem Texteditor öffnen

	# Konstanten fuer das ADW_CO2.py Modul
	temp_diff = 45
	datei_name = 'TL7176_1.asc'
	datei_beschreib = 'Probenname : Probe 2_1  10cmKorb 231.8g Probe 84.82g Korb'
    
   - s.o Zeilen /datei_name und datei_beschreib / entsprechend Anpassen
   - Datei ohne Veränderung des Names speichern.
   
   - Console öffnen
   - ins passende Verzeichniss mit cd-Befehl wechseln.
   - Messung mit 'python ADW_CO2.py' starten - Alte Variante 
   - nohup python -u ADW_PID_Adiabat.py </dev/null >/dev/null 2>&1 &


     erscheint auf der Console folgender Text
     1v3.2.32[May 26 2010]
     
     gefolgt von mehreren Zahlenreihen ist alles in Ordnung.
	 (gilt nicht für den nohup Aufruf!)

   - ADW_Ofen einschalten! (nicht Vergessen) 
     Überprüfen ob der Ofen auf dem externen Programmodus ist.
     Sollwert = Extern Programmmodus 2

   - Messung läuft maximal 200 Tage!!...wenn die Messung beendet werden soll in der Console mit CRTL-Z oder 
     (kill -KILL {Prozessnummer} wenn mit nohup Aufruf gestartet... {Prozessnummer} über TOP Befehl ermittel)


Erklärung der Dateistruktur der Savedatei.

Auszug aus Savedatei..:

" Probenname : Probenname : Probe 1_1  10cmKorb 223.8g Probe 84.82g Korb  
" Datum : 05.07.2012 um 15:09:01 Uhr
" ------------------------------------------------
7.4 ; 45.0  ; +0023.9 ; +0026.4 ; +0026.1 ; +0022.7 ; +0023.3 ; +0022.7 ; +0023.3 ; +0022.7 ; -16378.0
14.8 ; 45.0  ; +0023.9 ; +0026.3 ; +0026.1 ; +0022.7 ; +0023.3 ; +0022.7 ; +0023.3 ; +0022.7 ; -16378.0

Jede Zeile die mit " ist nur Kommentar..kann manuell beliebig erweitert werden.

Spalten
1 : Zeit in Sekunden
2 : Temperaturdifferenz zwischen Ofen und Probe (die Regelgröße NICHT die tatsächliche Differenz)
3 : T1 Ofentemperatur direkt an der Heizung
4 : T2 Temperatur in der Probenhälfte
5 : T3 Temperatur in der Probenmitte
6 : T4 Ablufttemperatur
7 : T5 Temperatur irgendwo im Ofenraum
8 : T6 Temperatur irgendwo im Ofenraum
9 :  T7 Temperatur irgendwo im Ofenraum
10 : frei
11 : CO-Wert (muss noch umgerechnet werden)



    
   
   
    

   
