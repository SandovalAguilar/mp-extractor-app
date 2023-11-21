import pandas as pd
import flet as ft

from distribution_table import table as t
from scripts import dataAnalyzer as da
from scripts import htmlToDataFrame as hd

tables = da.dataAnalyzer(hd.toDataFrame(
    'https://www.misprofesores.com/escuelas/UANL-FCFM_2263'))

grouped_table = t.groupedTable('tabla', tables.fullTable[['Promedio']])

print(grouped_table.table)
print(str(grouped_table.table['Intervals'].iloc[0]))