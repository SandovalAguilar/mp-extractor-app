import flet as ft
import pandas as pd
import mysql.connector
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column,LinearGradient,colors,DataColumn
from flet_core.control_event import ControlEvent




from scripts import dataAnalyzer as da
from scripts import htmlToDataFrame as hd
from distribution_table import table as dt
from charts import bar_chart as bc

#credenciales para la base de datos
conexion = mysql.connector.connect(user='uuvipz0v8e4x2axm', password='35UW4RDkqBWIy5NfT3Wp', host='bkzxz5yi2mqoyjhpjzcd-mysql.services.clever-cloud.com',database='bkzxz5yi2mqoyjhpjzcd',port='3306')



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

    #aqui va el login
    text_username: TextField = TextField(label='Usuario', text_align=ft.TextAlign.CENTER, width=230)
    text_password: TextField = TextField(label='Contrasena', text_align=ft.TextAlign.CENTER, width=230, password=True)
    Checkbox_showPassword: Checkbox = Checkbox(label='Mostrar Contrasena', value=False)
    button_login: ElevatedButton = ElevatedButton(text='Iniciar Secion', width=230, disabled=True)

    def Validate(e: ControlEvent) -> None:
        if all([text_username.value, text_password.value]):
            button_login.disabled=False
        else:
            button_login.disabled=True

        page.update()
    
    def ShowPassword(e: ControlEvent) ->None:
        if (Checkbox_showPassword.value == True):
            text_password.password=False
        else:
            text_password.password=True
        page.update()
    
    def Sumit(e: ControlEvent) -> None:

        cursor= conexion.cursor()
        cursor.execute("select * from Usuarios where user='"+text_username.value+"' and pass="+text_password.value)
        tabla=cursor.fetchone()
        print('usuario:', text_username.value)
        print('contra:', text_password.value)
        if(tabla):
            print('se pudo')
            conexion.close()
            page.clean()
            page.add(t)



    Checkbox_showPassword.on_change = ShowPassword
    text_password.on_change = Validate
    text_username.on_change = Validate
    button_login.on_click = Sumit


    container = ft.Container(
        ft.Column([
            ft.Text(value='    BIENVENIDO',text_align='center',size=30,weight ='w700',),
            ft.Container(text_username,padding=ft.padding.only(20,20)),
            ft.Container(text_password,padding=ft.padding.only(20,20)),
            ft.Container(Checkbox_showPassword,padding=ft.padding.only(20,20)),
            ft.Container(button_login,padding=ft.padding.only(20,20)),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
        
        border_radius=20,
        width=300,
        height=400,
        gradient= ft.LinearGradient([
            ft.colors.BLUE_50,
            ft.colors.BLUE_100,
            ft.colors.BLUE_200,
        ])

    )

    #termina login


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

    page.add(container)


if __name__ == "__main__":
    ft.app(target=main)  # view = ft.AppView.WEB_BROWSER)
