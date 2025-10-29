import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import re
import csv

#FUNCIÓN LECTURA DE IMAGEN
def read_image(image_path):
    # Leer imagen y convertir a RGB
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Invertir colores de la imagen
    img_inverted = cv2.bitwise_not(img_rgb)

    # Definir rango de color blanco para crear máscara
    blanco_bajo = np.array([190, 190, 190])
    blanco_alto = np.array([255, 255, 255])
    mask = cv2.inRange(img_inverted, blanco_bajo, blanco_alto)

    # Aplicar máscara para resaltar la etiqueta
    result_white = cv2.bitwise_and(img_inverted, img_inverted, mask=mask)

    # Extraer texto usando pytesseract OCR
    product_string = pytesseract.image_to_string(result_white)
    return product_string

#FUNCIONES PARA PROCESAMIENTO DE STRING

#EXTRACCIÓN MARCA
def extract_brand(text_string, brands_names):
    # Convertir todo el texto a mayúsculas para hacer la búsqueda insensible
    text_upper = text_string.upper()
    
    # Recorrer la lista de marcas y buscar coincidencia en el texto
    for brand in brands_names:
        if brand.upper() in text_upper:
            # Retornar la marca encontrada
            return brand
    
    # Si no se encontró ninguna marca, retornar None
    return None

#EXTRACCIÓN MODELO
def extract_model(text_string):
    # Patrón regex para buscar "Model" o "Model No" o "M/N"seguido del número de serie
    pattern_model = re.compile(r'(?:Model|Model No|M/N)\s*[:\-]?\s*(\S+)', re.IGNORECASE)
    
    # Buscar la primera coincidencia en el texto
    match = pattern_model.search(text_string)
    
    # Si se encontró, devolver el modelo sin espacios extras
    if match:
        return match.group(1).strip()
    
    # Si no se encontró, retornar None
    return None

#EXTRACCIÓN S/N
def extract_serial(text_string):
    # Patrón regex para buscar "SN" o "S/N" seguido del número de serie
    pattern_sn = re.compile(r'(?:SN|S/N)\s*[:\-]?\s*([A-Z0-9]+)', re.IGNORECASE)
    
    # Buscar la primera coincidencia en el texto
    match = pattern_sn.search(text_string)
    
    # Si se encontró, devolver el número de serie sin espacios extras
    if match:
        return match.group(1).strip()
    
    # Si no se encontró, retornar None
    return None

#FUNCIÓN PARA GUARDAR EN CSV
def save_product(brand, model, sn, csv_file):
    # Inicializar el ID del producto
    next_id = 1
    
    # Abrir el CSV en modo lectura
    with open(csv_file, mode='r', newline='') as f:
        # Leer todas las filas del CSV
        reader = csv.reader(f)
        rows = list(reader)
        
        # Si hay al menos una fila de datos, obtener el último ID
        if len(rows) > 1:
            last_row = rows[-1]
            next_id = int(last_row[0]) + 1  # Incrementar ID

    # Abrir CSV en modo append (agregar fila)
    with open(csv_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        # Escribir los datos del producto con el ID calculado
        writer.writerow([next_id, brand, model, sn])

    # Imprimir mensaje de confirmación
    print(f"Producto guardado: ID={next_id}, Brand={brand}, Model={model}, SN={sn}")