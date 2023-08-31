from bs4 import BeautifulSoup
import boto3
import pandas as pd
import datetime

def get_file():

    s3 = boto3.client('s3')
    bucket_name = 'khadajhinnnn'
    archivo_nombre = 'news/raw/'+datetime.datetime.now().strftime('%Y-%m-%d')+'.html'
    response = s3.get_object(Bucket=bucket_name, Key=archivo_nombre)
    # Leer el contenido del objeto (archivo)
    contenido = response['Body'].read().decode('utf-8')
    return contenido



def soup_process(contenido):
    soup = BeautifulSoup(contenido, 'html.parser')

    for span_etq in soup.find_all('span'):
        span_etq.extract()

    categoria = soup.find_all('div', class_='category-published')
    titulos = soup.find_all('h2', class_='title-container')
    enlaces = soup.find_all('a', class_='title page-link')

    lst_c = ['categoria']
    lst_t = ['titulo']
    lst_e = ['enlace']

    for c in categoria:
        lst_c.append(c.text)
    for t in titulos:
        lst_t.append(t.text)  
    for e in enlaces:
        lst_e.append('https://eltiempo.com'+e['href'])

    lst = [lst_c,lst_t,lst_e]

    l = 39

    while len(lst_c) < l:
        lst_c.append(None)
    while len(lst_t) < l:
        lst_t.append(None)

    return lst


def to_csv(lst):
    df = pd.DataFrame(lst[1:], columns=lst[0])
    archivo = df.to_csv(datetime.datetime.now().strftime('%Y-%m-%d')+'.csv', index=False)
    # Obtener la fecha actual
    fecha_actual = datetime.datetime.now()
    año = fecha_actual.year
    mes = fecha_actual.month
    dia = fecha_actual.day

    # Construir la ruta del objeto en S3
    ruta_objeto = f'headlines/final/year={año}/month={mes:02d}/{año:04d}-{mes:02d}-{dia:02d}.csv'

    s3 = boto3.client('s3')
    bucket_name = 'khadajhinnnn'
    # Subir el archivo en memoria a S3
    
    with open(csv, 'rb') as f:
        contenido = f.read()

    s3.upload_fileobj(BytesIO(contenido), bucket_name, ruta_objeto)

    print('Se ha subido correctamente el csv')

def main():
    to_csv(soup_process(get_file()))

main()
