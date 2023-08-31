from urllib.request import urlopen
import datetime
import boto3
from io import BytesIO


def get_response():
    # URL de la página a hacer web scraping
    return urlopen('https://www.eltiempo.com')
     
def upload_file(archivo_m,  bucket, archivo):
    s3 = boto3.client('s3')
    bucket_name = 'khadajhinnnn'
    # Subir el archivo en memoria a S3
    s3.upload_fileobj(archivo_m, bucket, 'news/raw/'+archivo)

def name_file():
    # Generamos el nombre del archivo usando la fecha actual
    fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
    nombre_archivo = f'{fecha_actual}.html'
    return nombre_archivo

def main():
    # Realizamos la solicitud GET a la URL
    response = get_response()

    # Verificamos si la solicitud fue exitosa
    if response.status == 200:
        # Leemos el contenido de la respuesta
        contenido = response.read()

        # Crear un objeto de tipo BytesIO para trabajar con el contenido en memoria
        archivo_m = BytesIO(contenido)

        upload_file(archivo_m,'khadajhinnnn',name_file())

        print('Web scraping completado. El contenido se ha subido al bucket')
    else:
        print('Error en la pagina web')


main()