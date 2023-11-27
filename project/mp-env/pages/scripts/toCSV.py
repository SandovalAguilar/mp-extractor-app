'''
 * Authors: Ismael Sandoval Aguilar, Edgar Iván Hinojosa Saldaña.
 * Created: 27.10.2022
'''

'''
file -- toCSV.py -- 
'''

# Librerias 
import pandas as pd
from datetime import date
from pathlib import Path

# Modulos
import scripts.dataAnalyzer as da
import scripts.htmlToDataFrame as hd

# Funcion principal
def to_csv(df, facultad, tableType):
    
    script_path = str(Path( __file__ ).absolute())
    today_date = str(date.today())
    df = df.to_csv( facultad + '_' + tableType + '_' + today_date + '.csv', index = False)

    print("Archivo creado satisfactoriamente en la ruta " + script_path + " con la fecha: " + today_date, flush = True)

    string = "Archivo creado satisfactoriamente en la ruta " + script_path + " con la fecha: " + today_date

    return string

# Este apartado solo debe utilizarse para realizar pruebas individuales del modulo
if __name__ == "__main__":
    
    tables = da.dataAnalyzer(hd.toDataFrame(
    'https://www.misprofesores.com/escuelas/UANL-FCFM_2263'))

    to_csv(tables.fullTable, 'FCFM', 'FULL')
