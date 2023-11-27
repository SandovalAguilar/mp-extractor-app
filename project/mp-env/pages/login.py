import flet as ft
import mysql.connector
import sql_config as sc

from flet import TextField, Checkbox, ElevatedButton
from flet_core.control_event import ControlEvent


class Fields:
    def __init__(self):
        self.text_username: TextField = TextField(
            label='Usuario', text_align=ft.TextAlign.CENTER, width=230)
        self.text_password: TextField = TextField(
            label='Contraseña', text_align=ft.TextAlign.CENTER, width=230, password=True)
        self.Checkbox_showPassword: Checkbox = Checkbox(
            label='Mostrar Contraseña', value=False)
        self.button_login: ElevatedButton = ElevatedButton(
            text='Iniciar Sesión', width=230, disabled=True)

        def text_username(self):
            return self.tex_username

        def text_password(self):
            return self.password

        def Checkbox_ShowPassword(self):
            return self.Checkbox_ShowPassword

        def buttton_login(self):
            return self.buttton_login


def verify_connector():
    try:
        credentials = sc.credentials()
        return credentials
    except Exception as error:
        print(error)


def validate(e: ControlEvent, page) -> None:

    if all([Fields().text_username.value, Fields().text_password.value]):
        Fields().button_login.disabled = False
    else:
        Fields().button_login.disabled = True

    page.update()


def show_password(e: ControlEvent, page) -> None:
    if (Fields().Checkbox_showPassword.value == True):
        Fields().text_password.password = False
    else:
        Fields().text_password.password = True

    page.update()


def submit(e: ControlEvent, page, credentials) -> None:
    cursor = credentials.cursor()
    cursor.execute("select * from Usuarios where user='"+Fields().text_username.value+"' and pass="+Fields().text_password.value)
    tabla = cursor.fetchone()
    print('usuario:', Fields().text_username.value)
    print('contraseña:', Fields().text_password.value)
    if (tabla):
        print('Done')
        credentials.close()
        page.clean()
        page.add(t)


def login_page(page):

    credentials = verify_connector()

    Fields().Checkbox_showPassword.on_change = show_password(ControlEvent, page)
    Fields().text_password.on_change = validate(ControlEvent, page)
    Fields().text_username.on_change = validate(ControlEvent, page)
    Fields().button_login.on_click = submit(ControlEvent, page, credentials)

    container = ft.Container(
        ft.Column([
            ft.Text(value='Bienvenido', text_align='center',
                    size=30, weight='w700',),
            ft.Container(Fields().text_username,
                         padding=ft.padding.only(20, 20)),
            ft.Container(Fields().text_password,
                         padding=ft.padding.only(20, 20)),
            ft.Container(Fields().Checkbox_showPassword,
                         padding=ft.padding.only(20, 20), alignment=ft.alignment.center),
            ft.Container(Fields().button_login,
                         padding=ft.padding.only(20, 20)),
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        border_radius=20)

    return container


def test_page(page: ft.Page):
    page.add(login_page(page))


if __name__ == "__main__":
    ft.app(target=test_page)  # view = ft.AppView.WEB_BROWSER)
