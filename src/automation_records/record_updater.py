
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from automation_records.custom_webdriver import CustomWebDriver

class RecordUpdater:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        #Se usa CustomWebDriver
        self.driver = CustomWebDriver().get_driver()
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        """Iniciar sesión en la plataforma"""
        print(f"Cargando la página: {self.url}")  # Verifica que Selenium intenta abrir la URL
        self.driver.get(self.url)
        
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("Página cargada correctamente")
        except:
            print("La página no carga")

        #Inicia sesión en la plataforma
        self.driver.get(self.url)
        self.driver.find_element(By.NAME, "UserName").send_keys(self.username)
        self.driver.find_element(By.NAME, "Password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)

        try: 
            permisos_btn = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//a[@class='btn btn-primary' and contains(@href,'tractview/167')]")))
            
            self.wait.until(EC.visibility_of(permisos_btn))
            self.driver.execute_script("arguments[0].scrollIntoView();", permisos_btn)
            time.sleep(1)
            permisos_btn.click()
            print("Se seleccionó la tarjeta de 'Genesis Permisos'")
            time.sleep(3)
        except Exception as e:
            print("No se pudo encontrar 'Genesis Permisos'")
            return
        
        self.driver.switch_to.window(self.driver.window_handles[-1])
        print("Se cambió a la pestaña de los expedientes de Permisos")
        time.sleep(5)

    def update_record(self, expediente_id, nuevos_datos):
        #Actualiza por el momento los COMENTARIOS, apartir de I.D. o No de Exp
        print("Actualización de expedientes")
        try:
            print(f"Buscando expediente en la plataforma: {expediente_id}")
            #Esperar a que cargue el primer grid
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "k-grid-content-locked")))

            scrollable_div = self.driver.find_element(By.CSS_SELECTOR, "div.k-grid-content.k-auto-scrollable")


            #tabla_html = self.driver.find_element(By.CSS_SELECTOR, "div.k-virtual-scrollable-wrap tbody tr").get_attribute("outerHTML")
            #print(f"Contenido HTML de la tabla: \n{tabla_html}")

            #Hacer scroll en pequeños pasos para cargar todas las filas
            
            filas_info = []
            try: 
                filas_info = self.driver.find_elements(By.CSS_SELECTOR, "div.k-virtual-scrollable-wrap tbody tr")
                print(f"Filas encontradas en la tabla: {len(filas_info)}")
            except Exception as e:

                if isinstance(filas_info, list):
                    print(f"Filas encontradas en la tabla: {len(filas_info)}")
                else:
                    print(f"Error: 'filas_info' no es una lista, sino un {type(filas_info)} ")
                    return

                print(f"No se pudieron obtener las filas: {e}")

            if not filas_info:
                print(f"No se encontraron filas en la tabla /nSaliendo de la función ")    
                return
            
            ultima_fila = filas_info[-1] if filas_info else None

            for _ in range(15): # Se hará scroll 10 veces
                if ultima_fila:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", ultima_fila)
                time.sleep(1)
                #Volver a obtener el número de filas después del scroll
                filas_info = self.driver.find_elements(By.CSS_SELECTOR, "div.k-virtual-scrollable-wrap tbody tr")
                print(f"Filas encontradas en la tabla después del scroll: {len(filas_info)}")

                #Si después de hacer scroll ya no se detectan filas, detener el ciclo
                if ultima_fila.get_attribute("data-uid") == filas_info[-1].get_attribute("data-uid"):
                    break

                ultima_fila = filas_info[-1]

            data_uid = None 

            for fila in filas_info:
                try:
                    data_uid_attr = fila.get_attribute("data-uid")
                    print(f"Revisando fila con data-uid: {data_uid_attr if data_uid_attr else 'No encontrado'}")

                    #Verificar en toda la fila
                    celdas = fila.find_elements(By.CSS_SELECTOR, "td")
                    for i, celda in enumerate(celdas):
                         
                        print(f"Celda {i} ({celda.get_attribute('data-field')}): {celda.text}")

                    #Buscar la celda NoExp
                    celda_noexp = fila.find_element(By.CSS_SELECTOR, 'td[data-field="NoExp"]')
                    noexp_valor = celda_noexp.text.strip()
                    print(f"Se encontró NoExp: {noexp_valor}")
                   
                    #Compara expediente_id(I.D. O No de Exp) del DataFrame
                    if noexp_valor == str(expediente_id):
                        print(f"Expediente {expediente_id} encontrado")
                        data_uid = data_uid_attr
                        break #Detenemos el ciclo si encontramos el expediente correcto
                except Exception as e:    
                    print(f"No se encontró 'NoExp' en esta fila. Error: {e}")
                    continue #Si la fila no contiene la celda NoExp pasa al siguiente
                        
            if data_uid is None:
                print(f"No se encontró el expediente {expediente_id} en la tabla.")
                return
        
            print(f"Expediente {expediente_id} encontrado con data-uid = {data_uid}.")

            #Buscar el botón correspondiente en `k-grid-content-locked`
            try:#-----------------------------------------------------------------------------------------------------------------------------
                btn_expediente = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"div.k-grid-content-locked tr[data-uid='{data_uid}'] .k-button"))
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", btn_expediente)
                time.sleep(1)
                
                print(" Intentando hacer clic en el botón...")
                btn_expediente.click()
                print(f"Se hizo clic en el botón del expediente {expediente_id}.")
            except:
                print(f"No se encontró el botón correspondiente para {expediente_id}.")
                return

            time.sleep(3)

            #Continuar con la actualización de expedientes
            cambios = False

            prefijo = expediente_id.split("-")[0]
            print(f"Procesando expediente {expediente_id} (Prefijo: {prefijo})")

            if prefijo == "IM":
                campos = {"Comentarios": nuevos_datos.get("COMENTARIOS")}
            elif prefijo == "CR":
                    campos = {"Comentarios": nuevos_datos.get("COMENTARIOS")}
            elif prefijo == "PM":
                    campos = {"Comentarios": nuevos_datos.get("COMENTARIOS")}

            else: 
                print(f"Prefijo '{prefijo}' no reconocido, no se actualizará expediente")
                return


            for campo, nuevo_valor in campos.items():
                if nuevo_valor is not None:
                    try:
                        elemento = self.driver.find_element(By.NAME, campo)
                        valor_actual = elemento.get_attribute("value")

                        if valor_actual != str(nuevo_valor):
                            elemento.clear()
                            elemento.send_keys(str(nuevo_valor))
                            cambios = True
                            print(f"Campo '{campo}', actualizado con: {nuevo_valor}")

                    except Exception as e:
                        print(f"No se encontró el campo '{campo}', omitiendo. Error: {e}")

            if cambios:
                self.driver.find_element(By.ID, "button1").click()
                time.sleep(2)
                print(f"Expediente {expediente_id} actualizado y cerrado.")
            else:
                print(f"Expediente {expediente_id} ya está actualizado")

            time.sleep(3)

        except Exception as e:
            print(f"Error al procesar el expediente {expediente_id}: {e}")


    def close(self):
        #Cierra el navegador
        if self.driver:
            self.driver.quit()
            print("Navegador cerrado correctamente")
    
