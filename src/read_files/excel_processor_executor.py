#Importa los paquetes necesarios
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from read_files.excel_processor import ExcelProcessor
from automation_records.record_updater import RecordUpdater

class ExcelProcessorExecutor:
    def __init__(self, file_path, url, username, password, skip_rows=0):
        #Se inicializan los métodos de Excel y Selenium
        self.processor = ExcelProcessor(file_path, skip_rows) #Manejo de excel
        self.updater = RecordUpdater(url, username, password) #Automatización con Selenium
        #self.output_path = "C:\\Practice\\Selenium\\files\\output.xlsx" #Ruta donde se guardará el archivo exportado
            
    def execute(self):
        #Limpieza y actualización de la plataforma

        self.processor.read_file() #Leer el archivo de excel
        self.processor.clean_data(thresh=10) #Limpiar dataframe, eliminando filas con con menos de 10 valores nulos
        #self.processor.print_dataframe() #Imprimir el DataFrame procesado
        self.updater.login()
        df_sheets = self.processor.get_data()
        
        
        #Iterar sobre los registros cada hoja 
                
        if df_sheets is None:
            print("No se pudieron obtener los datos del Excel")
            return
        
        for sheet_name, df in df_sheets.items():
            print(f"Procesando {sheet_name}")
            for index, row in df.iterrows():
                expediente_id = row["I.D."]  if "I.D." in row else row["No de exp"]
                nuevos_datos = {
                    "Comentarios": row.get("Comentarios")
                }
                print(f"Procesando expediente {expediente_id}")
                self.updater.update_record(expediente_id, nuevos_datos)

        """""
        #Exporta los datos procesados
        self.processor.export_dataframe("C:\\Practice\\Selenium\\files\\output.xlsx")
        """
        

        self.updater.close()
        

if __name__ == "__main__":

    file_excel= "C:\\Practice\\Selenium\\files\\GLOBAL SECCION A,B,C,D 28feb25_FN.xlsx"
    url = "https://services.steelshire.com/Skyray/Account/Login"
    username = "monica.salas" 
    password = "26Mo3110B09"

    executor = ExcelProcessorExecutor(file_excel, url, username, password, skip_rows=4)
    executor.execute()