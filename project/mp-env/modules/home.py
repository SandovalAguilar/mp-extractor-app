import flet as ft
import pandas as pd
import scripts.toCSV as tc
import scripts.toPDF as tp
import sql_config as sc

from flet import TextField, Checkbox, ElevatedButton
from flet_core.control_event import ControlEvent
from scripts import dataAnalyzer as da
from scripts import htmlToDataFrame as hd
from distribution_table import table as dt
from charts import bar_chart as bc

# Connector for the SQL database
connector = sc.credentials()

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


def home(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    fail_log = ft.Text(color=ft.colors.RED_400)

    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        light_mode_switch.label = (
            "Modo claro" if page.theme_mode == ft.ThemeMode.LIGHT else "Modo oscuro"
        )
        page.update()

    light_mode_switch = ft.Switch(label="Modo claro", on_change=theme_changed)

    text_username: TextField = TextField(
        label='Usuario', text_align=ft.TextAlign.CENTER, width=230)
    text_password: TextField = TextField(
        label='Contraseña', text_align=ft.TextAlign.CENTER, width=230, password=True)
    Checkbox_showPassword: Checkbox = Checkbox(
        label='Mostrar Contraseña', value=False)
    button_login: ElevatedButton = ElevatedButton(
        text='Iniciar Sesión', width=230, disabled=True)

    def validate(e: ControlEvent) -> None:
        if all([text_username.value, text_password.value]):
            button_login.disabled = False
        else:
            button_login.disabled = True
        fail_log.value = ''
        page.update()

    def show_password(e: ControlEvent) -> None:
        if (Checkbox_showPassword.value == True):
            text_password.password = False
        else:
            text_password.password = True
        page.update()

    def submit(e: ControlEvent) -> None:
        cursor = connector.cursor()
        cursor.execute("select * from Usuarios where user='" +
                       text_username.value+"' and pass='"+text_password.value+"'")
        tabla = cursor.fetchone()
        print('usuario:', text_username.value)
        print('contraseña:', text_password.value)
        if (tabla):
            print('Succes!')
            #connector.close()
            page.clean()
            page.add(t)
        else:
            print('Invalid')
            fail_log.value = "Usuario o contraseña incorrectos"
            page.update()

    def logout(e: ControlEvent) -> None:
        page.clean()
        page.add(container)

    Checkbox_showPassword.on_change = show_password
    text_password.on_change = validate
    text_username.on_change = validate
    button_login.on_click = submit

    container = ft.Container(
        ft.Column([
            ft.Text(value='Bienvenido', text_align='center',
                    size=30, weight='w700',),
            ft.Container(text_username, padding=ft.padding.only(20, 20)),
            ft.Container(text_password, padding=ft.padding.only(20, 20)),
            ft.Container(Checkbox_showPassword,
                         padding=ft.padding.only(20, 20), alignment=ft.alignment.center),
            ft.Container(button_login, padding=ft.padding.only(20, 20)),
            ft.Container(fail_log, padding=ft.padding.only(20, 20))
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        border_radius=20)

    # Tables
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

    lv_full = ft.ListView(expand=1, spacing=10, padding=20)
    lv_full.controls.append(datatable_full)

    # Buttons
    def button_report_clicked(e):
        dlg = ft.AlertDialog(title=ft.Text(tp.toPDF(tables)),
                             on_dismiss=lambda e: print("Dialog dismissed!"))
        page.dialog = dlg
        dlg.open = True
        page.update()

    def button_freq_table_clicked(e):
        dlg = ft.AlertDialog(title=ft.Text(tc.to_csv(mean_scores_table.table, 'FCFM', 'FREQUENCY')),
                             on_dismiss=lambda e: print("Dialog dismissed!"))
        page.dialog = dlg
        dlg.open = True
        page.update()

    def button_dataset_clicked(e):
        dlg = ft.AlertDialog(title=ft.Text(tc.to_csv(tables.fullTable, 'FCFM', 'FULL')),
                             on_dismiss=lambda e: print("Dialog dismissed!"))
        page.dialog = dlg
        dlg.open = True
        page.update()

    def button_statistics_clicked(e):
        dlg = ft.AlertDialog(title=ft.Text(tc.to_csv(tables.describeData, 'FCFM', 'STATISTICS')),
                             on_dismiss=lambda e: print("Dialog dismissed!"))
        page.dialog = dlg
        dlg.open = True
        page.update()

    def column_with_horiz_alignment(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.Container(
                    content=ft.ElevatedButton(
                        "Generar reporte (PDF)",
                        on_click=button_report_clicked,
                        icon="picture_as_pdf"),
                    alignment=ft.alignment.center,
                    width=400,
                    height=50
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Tabla de frecuencias (csv)",
                        on_click=button_freq_table_clicked,
                        icon="insert_chart",),
                    alignment=ft.alignment.center,
                    width=400,
                    height=50
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Dataset (csv)",
                        on_click=button_dataset_clicked,
                        icon="insert_chart"),
                    alignment=ft.alignment.center,
                    width=400,
                    height=50
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Estadística descriptiva (csv)",
                        on_click=button_statistics_clicked,
                        icon="insert_chart"),
                    alignment=ft.alignment.center,
                    width=400,
                    height=50
                )
            ]
        )

    def column_with_horiz_config(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.Container(
                    content=light_mode_switch,
                    alignment=ft.alignment.center,
                    width=150,
                    height=50
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Cerrar sesión",
                        on_click=logout,
                        icon="POWER_SETTINGS_NEW_SHARP",
                        icon_color="RED",
                        color="RED_300"),
                    alignment=ft.alignment.center_left,
                    width=150,
                    height=50
                )
            ]
        )

    t = ft.Tabs(
        selected_index=1,
        animation_duration=180,
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
                text="Generar reporte",
                content=ft.Container(content=column_with_horiz_alignment(ft.CrossAxisAlignment.CENTER),
                                     alignment=ft.alignment.center)
            ),
            ft.Tab(
                text="Configuración",
                content=ft.Container(content=column_with_horiz_config(ft.CrossAxisAlignment.CENTER),
                                     alignment=ft.alignment.center), 
            )
        ],
        expand=1,
    )

    page.add(container)


def start():
    #ft.app(target=home, view=ft.AppView.WEB_BROWSER)
    ft.app(target=home)


if __name__ == "__main__":
    start()
