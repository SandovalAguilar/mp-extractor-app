import scripts.htmlToDataFrame as hd
import scripts.dataAnalyzer as da
import dataframe_image as dfi

from fpdf import FPDF
from datetime import date
from pathlib import Path


class PDF(FPDF):
    def header(self):
        self.image('fcfm.png', w=15)
        self.set_font('Arial', 'B', 24)
        self.set_xy(0, 0)
        self.cell(200, 40, "Reporte de datos", 0, 0, 'R')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Pag.' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def toPDF(df):
    dfi.export(df.describeData, 'describe_table.png', max_rows=10)
    dfi.export(df.minTable.head(10), 'min_table.png', max_rows=10)
    dfi.export(df.maxTable.head(10), 'max_table.png', max_rows=10)

    pdf = PDF()
    pdf.add_page()
    pdf.alias_nb_pages()
    pdf.set_font('Arial', '', 12)
    pdf.cell(60, 40, 'Fecha de creación: ' + f'{date.today():%d-%m-%Y}')

    pdf.image('describe_table.png', x=70, y=50, w=60)
    pdf.image('max_table.png', x=30, y=120, w=140)
    pdf.image('min_table.png', x=30, y=200, w=140)

    script_path = str(Path(__file__).absolute())
    today_date = str(date.today())

    pdf.output('reporte_' + today_date + '.pdf', 'F')

    print('PDF creado satisfactoriamente en la ruta ' +
          script_path + " con la fecha: " + today_date)

    string = 'PDF creado satisfactoriamente en la ruta ' + script_path + " con la fecha: " + today_date
    
    return string

# Este apartado solo debe utilizarse para realizar pruebas individuales del modulo
if __name__ == "__main__":

    tables = da.dataAnalyzer(hd.toDataFrame(
        'https://www.misprofesores.com/escuelas/UANL-FCFM_2263'))

    toPDF(tables)
