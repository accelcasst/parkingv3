from random import sample
from flask import Flask
from flask import render_template, request, redirect, Response, url_for, session, jsonify
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb


#Conexion BD para CRUD
app = Flask(__name__,template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = '541219066'
app.config['MYSQL_DB'] = 'estacion'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


#-----------------------------------------------------

#Creando una funcion para obtener la lista de carros.
def listaCarros():
    cur = mysql.connection.cursor()

    querySQL = "SELECT * FROM carros ORDER BY id DESC"
    cur.execute(querySQL) 
    resultadoBusqueda = cur.fetchall() #fetchall () Obtener todos los registros
    totalBusqueda = len(resultadoBusqueda) #Total de busqueda
    
    cur.close() #Cerrando conexion SQL
    
    return resultadoBusqueda




def updateCarro(id=''):
        
        cursor  = mysql.connection.cursor()
        
        cursor.execute("SELECT * FROM carros WHERE id = %s LIMIT 1", [id])
        resultQueryData = cursor.fetchone() #Devolviendo solo 1 registro
        return resultQueryData
    
    
    
def registrarCarro(marca='', modelo='', year='', color='', puertas='', favorito='', nuevoNombreFile=''):       
       
        cursor  = mysql.connection.cursor()
        print("Prueba")
        print(puertas)
        print(favorito)
            
        sql         = ("INSERT INTO carros (marca, modelo, year, color, entrada, salida, foto) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        valores     = (marca, modelo, year, color, puertas, favorito, nuevoNombreFile)
        print(valores)
        cursor.execute(sql, valores)
        
        cursor.close() #Cerrando conexion SQL
        
        
        resultado_insert = cursor.rowcount #retorna 1 o 0
        ultimo_id        = cursor.lastrowid #retorna el id del ultimo registro
        return resultado_insert
  

def detallesdelCarro(idCarro):
       
        cursor  = mysql.connection.cursor()
        
        cursor.execute("SELECT * FROM carros WHERE id ='%s'" % (idCarro,))
        resultadoQuery = cursor.fetchone()
        cursor.close() #cerrando conexion de la consulta sql
        
        
        return resultadoQuery
    
    

def  recibeActualizarCarro(marca, modelo, year, color, puertas, favorito, nuevoNombreFile, idCarro):
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE carros
            SET 
                marca   = %s,
                modelo  = %s,
                year    = %s,
                color   = %s,
                puertas = %s,
                favorito= %s,
                foto    = %s
            WHERE id=%s
            """, (marca, modelo, year, color, puertas, favorito, nuevoNombreFile,  idCarro))
        
        
        cur.close() #cerrando conexion de la consulta sql
        
        resultado_update = cur.rowcount #retorna 1 o 0
        return resultado_update
 

#Crear un string aleatorio para renombrar la foto 
# y evitar que exista una foto con el mismo nombre
def stringAleatorio():
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio