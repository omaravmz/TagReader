# TagReader

## Descripción

TagReader es un pequeño automatizador para leer etiquetas de cajas de laptops/computadoras desde fotografías usando procesamiento de imagen y OCR (pytesseract). A partir de la imagen intenta extraer tres campos principales: marca, modelo y número de serie (S/N), y guarda los productos detectados en `products.csv`.

Está pensado para inventarios de tienda y pruebas rápidas sobre fotos tomadas a las cajas.

## Características

- Detecta texto en una región de la imagen tras un preprocesado básico (inversión y máscara de blancos).
- Extrae marca (comparando con una lista de marcas), modelo (regex para campos 'Model', 'M/N', etc.) y S/N (regex para 'SN' o 'S/N').
- Guarda registros en `products.csv` con un ID incremental.

## Estructura del proyecto

- `functions.py` - Lógica principal: lectura y preprocesado de imagen, extracción de marca/modelo/SN y función para guardar en CSV.
- `main.py` - Ejemplos de uso: procesa imágenes de `public/` y añade filas a `products.csv`.
- `products.csv` - CSV donde se almacenan los productos. Contiene cabecera y filas con ID, MARCA, MODELO, S/N.
- `requirements.txt` - Dependencias Python usadas por el proyecto.
- `public/` - Fotos de ejemplo (no incluidas en este README).

## Requisitos

- Python 3.8+ (probado con 3.10+).
- Tesseract OCR instalado en el sistema (pytesseract es un wrapper que requiere el ejecutable).

Dependencias Python (ver `requirements.txt`):

- opencv-python
- numpy
- pillow
- pytesseract
- matplotlib

Instalación del paquete de Python:

En PowerShell (Windows):

```powershell
python -m pip install -r requirements.txt
```

Instalación de Tesseract (Windows):

1. Descargar el instalador de Tesseract (recomendado: build de UB Mannheim) desde:
	https://github.com/UB-Mannheim/tesseract/wiki
2. Instalar y añadir el directorio de instalación a la variable de entorno PATH, por ejemplo:
	C:\Program Files\Tesseract-OCR
3. Alternativamente, puede indicar en el código la ruta completa con:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## Uso básico

El archivo `main.py` ya contiene ejemplos que leen tres imágenes de `public/` y guardan resultados en `products.csv`.

Para ejecutar los ejemplos:

```powershell
python main.py
```

Ejemplo de lo que hace el flujo (resumen):

1. `read_image(path)` — abre la imagen, convierte a RGB, la invierte y aplica una máscara para conservar zonas claras.
2. `pytesseract.image_to_string(...)` — extrae texto de la imagen procesada.
3. `extract_brand(text, brand_list)` — busca la primera marca conocida dentro del texto.
4. `extract_model(text)` — intenta capturar el valor del modelo con expresiones regulares (buscando `Model`, `M/N`, etc.).
5. `extract_serial(text)` — extrae el S/N con una expresión regular que busca `SN` o `S/N` seguido de caracteres alfanuméricos.
6. `save_product(brand, model, sn, csv_file)` — agrega una fila al CSV con un ID incremental.

## Formato de `products.csv`

El CSV tiene el siguiente formato (cabecera):

```
ID, MARCA, MODELO, S/N
```

Ejemplo de contenido:

```
1,HUAWEI,KLVL-W76W,C5M8D196B9000134
2,HP,16-f0010ca,5CB1234FGH9012
3,SAMSUNG,NP960XFH,GSC1A2B3HGH5K67
```

Si `products.csv` no existe o está vacío, cree una cabecera manualmente antes de ejecutar (o ejecute el script y verifique que `save_product` hace append correctamente).

## Casos borde y limitaciones

- El OCR falla con fotos borrosas, ángulos extremos, etiquetas dañadas o fondos muy ruidosos.
- Si la marca no está en la lista `brand_names`, no será detectada. Añada marcas a la lista en `main.py` o implemente un diccionario más amplio.
- Las expresiones regulares actuales buscan patrones comunes (`Model`, `SN`), pero no cubren todos los formatos. Pueden ajustarse para casos locales.

## Depuración y troubleshooting

- Si `pytesseract` lanza error indicando que no encuentra `tesseract`, asegúrese de que el ejecutable está en PATH o configure `pytesseract.pytesseract.tesseract_cmd` con la ruta completa.
- Si la salida de OCR está vacía o contiene muchos caracteres raros, pruebe a visualizar la imagen preprocesada y ajustar los umbrales de la máscara (valores en `functions.read_image`).

## Licencia y contribuciones

Este repositorio no contiene una licencia explícita. Añada un `LICENSE` si desea abrirlo. Las contribuciones son bienvenidas: abra issues o PRs con mejoras y tests.
