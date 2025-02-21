
from excel_processor import ExcelProcessor


class ExcelProcessorExecutor:
    def __init__(self, file_path, skip_rows=0):
        
        
        self.processor = ExcelProcessor(file_path, skip_rows)
            
    def execute(self):
    
        #Leer el archivo de excel
        self.processor.read_file()

        #Limpiar los datos del dataframe, eliminando las filas con con menos de 10 valores nulos
        self.processor.clean_data(thresh=10)

        #Imprimir el DataFrame procesado
        self.processor.print_dataframe()
        #"""
        #Exporta los datos procesados
        self.processor.export_dataframe("C:\\Practice\\Selenium\\files\\output.xlsx")
        #"""

if __name__ == "__main__":

    file_excel= "C:\\Practice\\Selenium\\files\\GLOBAL SECCION A,B,C,D 17ene25_FN.xlsx"

    executor = ExcelProcessorExecutor(file_excel, skip_rows=4)
    executor.execute()