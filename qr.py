# Importamos la biblioteca
import qrcode
import random

# Creamos el código QR y entre comillas simples escribimos la cadena que se va a codificar, en este caso usamos la dirección de nuestro blog
def generetor(string):
    
    img = qrcode.make(string)
    num = random.randint(1, 1000)
    list_names = [2]
    while num in list_names:  
        num = random.randint(1, 1000)  

    name = str(num) +'.png'
    # Abrimos un archivo en modo escritura que es donde se guardará nuestro código.
    with open(name, 'wb') as img_file:
        # Guardamos nuestro código en el archivo que creamos y lo cerramos
        img.save(img_file)
        img_file.close
    return name
