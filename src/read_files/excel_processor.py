# Import packages necessarily
import pandas as pd
import warnings

pd.options.display.date_dayfirst = True

class ExcelProcessor:
    def __init__(self, file_path, skip_rows=4):
        self.file_path = file_path
        self.skip_rows = skip_rows
        self.sheets = {}
        

    def read_file(self):
        warnings.simplefilter(action='ignore', category=UserWarning)
        try:
            self.sheets = pd.read_excel(self.file_path, sheet_name= None, skiprows=self.skip_rows)
            print("Archivo leído con éxito")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    def clean_data(self, thresh=10):

        if self.sheets:
            for sheet_name, df in self.sheets.items():
                df.dropna(thresh=thresh, inplace=True)
                print("Datos limpios" )
        else:
            print("Error: No hay datos que limpiar")
   
        
    def print_dataframe(self):
        if self.sheets:
            for sheet_name, df in self.sheets.items():
                print(f"\nHoja: {sheet_name}")
                print(df)
        else:
            print("Error: No se ha cargado ningún dataframe para imprimir")

    def get_data(self):
        #Devuelve el dataframe
        if self.sheets is None:
            print("Error: No se pudo cargar el DataFrame")
            return None
        return self.sheets

"""
    def export_dataframe(self, output_path):
        try: 
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                for sheet_name, df in self.sheets.items():
                    df.rename(columns=lambda x: x.strip(), inplace=True)
                    #Cambiar a datetime
                    df['FECHA DE INGRESO REAL'] = pd.to_datetime(df['FECHA DE INGRESO REAL'], errors='coerce')
                    #Dar nuevo formato a la celda FECHA DE INGRESO REAL
                    df['FECHA DE INGRESO REAL'] = df['FECHA DE INGRESO REAL'].dt.strftime('%d/%m/%Y')

                    #Cambiar a datetime
                    df['FECHA DE OBTENCIÓN REAL'] = pd.to_datetime(df['FECHA DE OBTENCIÓN REAL'], errors='coerce')
                    #Dar nuevo formato a la celda FECHA DE INGRESO REAL
                    df['FECHA DE OBTENCIÓN REAL'] = df['FECHA DE OBTENCIÓN REAL'].dt.strftime('%d/%m/%Y')

                     #Cambiar a datetime
                    df['VIGENCIA'] = pd.to_datetime(df['VIGENCIA'], errors='coerce')
                    #Dar nuevo formato a la celda FECHA DE INGRESO REAL
                    df['VIGENCIA'] = df['VIGENCIA'].dt.strftime('%d/%m/%Y')

                     #Cambiar a datetime
                    
                    #Dar nuevo formato a la celda FECHA DE INGRESO REAL
                    
                    df['LONGITUD (KM)'] = pd.to_numeric(df['LONGITUD (KM)'], errors='coerce')*100

                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            
            print(f"Archivo exportado con éxito en {output_path}")
        except Exception as e:
            print(f"Error al exportar el archivo: {e}")
    
"""
   