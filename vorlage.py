"""
Created on 08.08.2012

@author: rened
Vorgabendatei fuer die CO-Messung
"""

# Konstanten fuer das ADW_CO2.py Modul
temp_diff = 25.
datei_name = 'TL9582_3x.asc'
datei_beschreib = 'Probenname : Wiederholung mit 40gK und 188g Probe '

# Konstanten fuer das Auswert.py Skript

show_co = True
# Zeigt als zweites Diagramm das CO-Diagramm

# show_kin = False
# Zeigt als zweites Diagamm den Kissingerplot

# Umrechnung fur den CO-Wert
def CO_Value(Li_Wert):
    return ((0.00028*Li_Wert+4.5)*10.0)+0.85
