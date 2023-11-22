import flet as ft
import pandas as pd

from scripts import dataAnalyzer as da
from scripts import htmlToDataFrame as hd
from distribution_table import table as dt
from charts import bar_chart as bc

tables = da.dataAnalyzer(hd.toDataFrame(
    'https://www.misprofesores.com/escuelas/UANL-FCFM_2263'))

mean_scores_table = dt.groupedTable('tabla', tables.fullTable[['Promedio']])

def headers(df: pd.DataFrame) -> list:
    return [ft.DataColumn(ft.Text(header)) for header in df.columns]


def rows(df: pd.DataFrame) -> list:
    rows = []
    for index, row in df.iterrows():
        rows.append(ft.DataRow(
            cells=[ft.DataCell(ft.Text(row[header])) for header in df.columns]))
    return rows


def main(page: ft.Page):
    datatable_max = ft.DataTable(columns=headers(
        tables.maxTable), rows=rows(tables.maxTable))
    datatable_min = ft.DataTable(columns=headers(
        tables.minTable), rows=rows(tables.minTable))
    datatable_describe = ft.DataTable(columns=headers(
        tables.describeData), rows=rows(tables.describeData))
    datatable_full = ft.DataTable(columns=headers(
        tables.fullTable), rows=rows(tables.fullTable))

    lv_max = ft.ListView(expand=1, spacing=10, padding=20)
    lv_max.controls.append(datatable_max)

    lv_min = ft.ListView(expand=1, spacing=10, padding=20)
    lv_min.controls.append(datatable_min)

    '''
    lv_describe = ft.ListView(expand=1, spacing=10, padding=20)
    lv_describe.controls.append(datatable_describe)
    '''

    lv_full = ft.ListView(expand=1, spacing=10, padding=20)
    lv_full.controls.append(datatable_full)

    t = ft.Tabs(
        selected_index=1,
        animation_duration=150,
        scrollable=True,
        tabs=[
            ft.Tab(
                text="Mejores profesores",
                content=ft.Container(
                    content=lv_max, alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                text="Peores profesores",
                content=ft.Container(
                    content=lv_min, alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                text="Estadística descriptiva",
                content=ft.Container(
                    content=datatable_describe, alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                text="Tabla completa",
                content=ft.Container(
                    content=lv_full, alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                text="Histograma",
                content=bc.generate_bar_chart(mean_scores_table)
                ),
            ft.Tab(
                text="Generar PDF"
            )
        ],
        expand=1,
    )

    page.add(t)


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)  # view = ft.AppView.WEB_BROWSER)
