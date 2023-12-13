
from datetime import datetime
from functools import wraps
from flask import Flask, current_app, make_response, send_from_directory
from flask import render_template, request, redirect, Response, url_for, session, jsonify
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
from controller.controllerCarro import *
import qrcode
import pdfkit
from reportlab.pdfgen import canvas
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash, check_password_hash


#Para subir archivo tipo foto al servidor
import os
from werkzeug.utils import secure_filename 

# Ruta a la carpeta de códigos QR
QR_FOLDER = os.path.join(os.getcwd(), 'qrcodes')

# Verificar si la carpeta existe, si no, crearla
if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)


#Conexion BD para login
app = Flask(__name__,template_folder='template')
app.config['IMAGES_FOLDER'] = 'QRs'

app.config['MYSQL_HOST'] = 'estacionamiento.ck7ydebwk6vz.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'cisco123'
app.config['MYSQL_DB'] = 'estacionamiento'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


#-----------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')   

@app.route('/admin')
def admin():
    return render_template('admin.html')   




#-----------------------------

def login_required(role=None, sucursal=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if 'username' in session:
                user_role = session.get('id_rol')
                user_sucursal = session.get('id_sucursal')

                if role and user_role != role:
                    return redirect(url_for('dashboard'))

                if sucursal and user_sucursal != sucursal:
                    return redirect(url_for('dashboard'))

                return view_func(*args, **kwargs)
            else:
                return redirect(url_for('login'))
        return wrapper
    return decorator


# ACCESO---LOGIN
@app.route('/acceso-login', methods= ["GET", "POST"])
def login():
   
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
       
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s', (_correo,))
        account = cur.fetchone()

        if account and check_password_hash(account['password'], _password):
            session['logueado'] = True
            session['id'] = account['id']
            session['id_rol'] = account['id_rol']
            session['id_sucursal'] = account['id_sucursal']
            session['username'] = account['username']

            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', mensaje="Usuario O Contraseña Incorrectas")

# ...


@app.route('/dashboard')

@login_required()
def dashboard():
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')

    if session['id_rol']==1:
                cur = mysql.connection.cursor()

                
                return render_template("admin.html", id_rol=id_rol_login, id_sucursal=id_sucursal_login,username=username_login)
    
    elif session ['id_rol']==2:
                return render_template("usuario.html", id_rol=id_rol_login, id_sucursal=id_sucursal_login,username=username_login)
    elif session ['id_rol']==3:
                return render_template("superadmin.html", id_rol=id_rol_login, id_sucursal=id_sucursal_login,username=username_login)

    






#registro usuarios---
@app.route('/registro',  methods= ["GET", "POST"])
@login_required()
def registro():
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
    #----------------------------------------------
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM sucursal")
    sucursal = cur.fetchall()
    cur.close()
    return render_template('registro.html',sucursal=sucursal, username=username_login,id_rol=id_rol_login  )  

@app.route('/crear-registro', methods= ["GET", "POST"])
@login_required()
def crear_registro(): 
    
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
    #----------------------------------------------
    
    nombre=request.form['nombre']
    correo=request.form['txtCorreo']
    
    rol=request.form['rol']
    sucursal=request.form['sucursal']
    password = request.form['txtPassword']
    hashed_password = generate_password_hash(password)
    print(hashed_password)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (username, correo, password, id_rol, id_sucursal) VALUES (%s,%s, %s, %s, %s)",
                (nombre, correo, hashed_password, rol, sucursal))
    mysql.connection.commit()

    return redirect(url_for('listar', mensaje2="Usuario Registrado Exitosamente"))
#-----------------------------------

#-----LISTAR USUARIOS-------------
@app.route('/listar', methods= ["GET", "POST"])
@login_required()
def listar(): 
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#----------------------------------- 
    cur = mysql.connection.cursor()
    cur.execute("SELECT usuarios.id AS id_usuario, usuarios.username, usuarios.correo, usuarios.password, roles.descripcion AS nombre_rol, sucursal.descripcion AS nombre_sucursal FROM usuarios JOIN roles ON usuarios.id_rol = roles.id_rol JOIN sucursal ON usuarios.id_sucursal = sucursal.id_sucursal;")
    usuarios = cur.fetchall()
    cur.close()
    
    
    
    return render_template("listar_usuarios.html",sucursal=id_sucursal_login, username=username_login,id_rol=id_rol_login,usuarios=usuarios)
#----------------------------------


@app.route('/edit_usuario/<int:id_usuario>', methods=['GET', 'POST'])
@login_required()
def edit_usuario(id_usuario):
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#----------------------------------- 
    cur = mysql.connection.cursor()
    cur.execute("SELECT usuarios.id AS id_usuario, usuarios.username, usuarios.correo, usuarios.password, roles.descripcion, usuarios.id_rol, sucursal.id_sucursal, roles.descripcion AS nombre_rol, sucursal.descripcion AS nombre_sucursal FROM usuarios JOIN roles ON usuarios.id_rol = roles.id_rol JOIN sucursal ON usuarios.id_sucursal = sucursal.id_sucursal WHERE usuarios.id= %s", (id_usuario,))
    usuario = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM sucursal")
    sucursales = cur.fetchall()
    cur.close()
    
    if request.method == 'POST':
       

        # Calcular el costo
        
        nombre = usuario['username']
        correo = usuario['correo']
        password = usuario['password']
        rol = request.form['rol']
        
        print('espacio')
        
       

        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET username=%s,correo=%s,password=%s,id_rol=%s WHERE id= %s", (nombre,correo,password,rol,id_usuario))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('listar'))

        
    
    
    
    return render_template('editar_usuario.html', usuario=usuario, sucursals=sucursales, sucursal=id_sucursal_login, username=username_login,id_rol=id_rol_login)



#----------------------------------

@app.route('/delete_usuario/<int:id_usuario>')
@login_required()
def delete_usuario(id_usuario):
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#-----------------------------------     
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listar'))

#######################################  
#####Estacionamiento####
####################################
@app.route('/prueba')
@login_required()
def index():
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#-----------------------------------     
    id = session.get('id')
    id_rol = session.get('id_rol')
    id_sucursal = session.get('id_sucursal')
    username=session.get('username')
    if id_rol == 3:
        print(type(id_sucursal))
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cars  ")
        cars = cur.fetchall()
        cur.close()
        return render_template('CRUD.html', cars=cars, sucursal=id_sucursal_login, username=username_login,id_rol=id_rol_login)
    else:
        print(type(id_sucursal))
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cars WHERE id_sucursal = %s and estado='no pagado'", (id_sucursal,))
        cars = cur.fetchall()
        cur.close()
        return render_template('CRUD.html', cars=cars, sucursal=id_sucursal_login, username=username_login,id_rol=id_rol_login)
    
@app.route('/add', methods=['POST'])
@login_required()
def add():
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#----------------------------------- 
    id = session.get('id')
    id_rol = session.get('id_rol')
    id_sucursal = session.get('id_sucursal')
    username=session.get('username')
    Placa = request.form['Placa']
    entry_time = request.form['Entrada']
    print("######################################")
    print(entry_time)
    print(Placa)
    print(id_sucursal)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO cars (Placa, entry_time, id_sucursal, estado) VALUES (%s, %s, %s,'no pagado')", (Placa, entry_time,id_sucursal))
    mysql.connection.commit()
    print(cur)
    cur.close()
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT id FROM cars ORDER BY id DESC LIMIT 1')
    id_registro = cur.fetchone()
    id_registro = id_registro['id']
    print(type (id_registro))
    print(id_registro)
    # Generar código QR
    return redirect(url_for('ticket',id_registro=id_registro))

@app.route('/qrcodes/<filename>')
@login_required()
def serve_image(filename):
    return send_from_directory('qrcodes', filename)


@app.route('/ticket/<int:id_registro>', methods=['GET', 'POST'])
@login_required()

def ticket(id_registro):
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#----------------------------------- 
    
    # Generar código QR
    cur = mysql.connection.cursor()
    cur.execute('SELECT id FROM cars ORDER BY id DESC LIMIT 1')
    car = cur.fetchone()
    home = request.url_root
    data = f'{home}:5000/ticket/{car}'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")


    # Guardar la imagen en una carpeta
    img_path = os.path.join(QR_FOLDER, f'qr_{id_registro}.png')
    img.save(img_path)

    cur = mysql.connection.cursor()
    cur.execute("UPDATE cars SET qr_image_path = %s WHERE id = %s", (img_path,id_registro))
    mysql.connection.commit()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cars WHERE id = %s", (id_registro,))
    car2 = cur.fetchone()

    return render_template('ticket.html', car2=car2, os=os,)

@app.route('/ticket_pagado/<int:id_registro>', methods=['GET', 'POST'])
@login_required()
def ticket_pagado(id_registro):
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#----------------------------------- 
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cars WHERE id = %s", (id_registro,))
    car2 = cur.fetchone()
    
    return render_template('ticket.html', car2=car2, os=os)




@app.route('/descargar_pdf/<int:car_id>', methods=['POST'])
@login_required()
def descargar_pdf(car_id):
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#----------------------------------- 
    cursor = mysql.connection.cursor()
    print(type(car_id))
    print({car_id})
    # Obtener registros de la base de datos
    cursor.execute('SELECT * FROM cars WHERE id = %s', (car_id, ))
    registros = cursor.fetchall()

    cursor.close()

    nombre=('registro')
    nombre2=(str(car_id))
    nombrepdf=(nombre+nombre2+'.pdf')


    # Crear un PDF con la información de los registros
    pdf_path = os.path.join(os.getcwd(), nombrepdf)
    generar_pdf(registros, pdf_path)

    # Enviar el PDF como respuesta para descargar
    response = make_response(send_from_directory(os.getcwd(), nombrepdf, as_attachment=True))
    return response
    
    

# Función para generar un PDF con la información de los registros
@login_required()
def generar_pdf(registros, pdf_path):
    pdf = canvas.Canvas(pdf_path, pagesize=letter)
    pdf.setTitle("Registros")
    print(registros)

    y_position = 750
    for registro in registros:
        pdf.drawString(100, y_position, f"ID: {registro['id']}")
        pdf.drawString(100, y_position - 20, f"Placa: {registro['Placa']}")
        pdf.drawString(100, y_position - 40, f"Entrada: {registro['entry_time']}")
        pdf.drawString(100, y_position - 60, f"N.sucursal: {registro['id_sucursal']}")


        qr_image_path = registro['qr_image_path']
        if os.path.exists(qr_image_path):
            pdf.drawImage(ImageReader(qr_image_path), 100, y_position - 200, width=100, height=100)

        y_position -= 100  # Ajusta el espacio según sea necesario

    pdf.save()
    

@app.route('/update/<int:car_id>', methods=['POST'])
@login_required()
def update(car_id):
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#----------------------------------- 
    exit_time = datetime.now()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE cars SET exit_time = %s, estado= Pagado WHERE id = %s", (exit_time, car_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('prueba'))

@app.route('/edit/<int:car_id>', methods=['GET', 'POST'])
@login_required()
def edit(car_id):
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#----------------------------------- 

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
    car = cur.fetchone()
    cur.close()

    return render_template('edit.html', car=car)

@app.route('/pagar/<int:car_id>', methods=['POST'])
@login_required()
def pagar(car_id):
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#----------------------------------- 

    if request.method == 'POST':
        entrada = datetime.strptime(request.form['entry_time'], "%Y-%m-%d   %H:%M:%S")
        salida = datetime.strptime(request.form['exit_time'], "%Y-%m-%dT%H:%M")


        try:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE cars SET exit_time = %s, estado = 'Pagado' WHERE id = %s", (salida, car_id))
            mysql.connection.commit()

            # Resta de tiempo
            diferencia = salida - entrada

            tolerancia = timedelta(minutes=15)
            primera_hora = timedelta(hours=2)
            costo_base = 20.0
            costo_hora_adicional = 20.0

            print(diferencia)

            if diferencia <= tolerancia:
                costo_total = 0.0  # Sin costo dentro de la tolerancia
            
            else:
                tiempo_en_tolerancia = max(timedelta(), diferencia - tolerancia)
                horas_parciales = max(timedelta(), tiempo_en_tolerancia - primera_hora)

                horas_completas = horas_parciales.total_seconds() // 3600

                costo_total = costo_base + (horas_completas * costo_hora_adicional)

            

            cur.execute("UPDATE cars SET total = %s, estado = 'Pagado' WHERE id = %s", (costo_total, car_id))
            mysql.connection.commit()
            
        

        except Exception as e:
            # Handle the exception, e.g., log it or return an error response.
            return render_template('error.html', error=str(e))
        finally:
            cur.close()
        return redirect(url_for('ticket_pagado', id_registro=car_id))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
    car = cur.fetchone()
    cur.close()

    return render_template('edit.html', car=car)

@app.route('/delete/<int:car_id>')
@login_required()
def delete(car_id):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cars WHERE id = %s", (car_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))


############################################################
#####################Pension##############################
#############################################################




####Calcular_pago_pension######

# Ruta principal - Lista de autos
@app.route('/pension')
@login_required()
def pension():
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#----------------------------------- 
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pension")
    autos = cur.fetchall()
    cur.close()
    return render_template('pension.html', autos=autos)

# Ruta para agregar un nuevo auto
@app.route('/agregar_pension', methods=['GET', 'POST'])
@login_required()
def agregar_pension():
    if request.method == 'POST':
        placa = request.form['placa']
        fecha_entrada = request.form['entrada']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pension (placa, fecha_entrada) VALUES (%s, %s)", (placa, fecha_entrada))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('ticket_pension'))
    return render_template('agregar_pension.html')


#####PDF pension#####
@app.route('/qrcodes_pension/<filename>')
@login_required()
def serve_image_pension(filename):
    return send_from_directory('qrcodes', filename)


@app.route('/ticket_pension', methods=['GET', 'POST'])
@login_required()
def ticket_pension():

    cur = mysql.connection.cursor()
    cur.execute('SELECT id FROM pension ORDER BY id DESC LIMIT 1')
    id_registro = cur.fetchone()
    id_registro = id_registro['id']
    print(type (id_registro))
    print(id_registro)
    # Generar código QR
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pension WHERE id = %s", (id_registro,))
    car = cur.fetchone()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(car)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")


    # Guardar la imagen en una carpeta
    img_path = os.path.join(QR_FOLDER, f'qr_{id_registro}.png')
    img.save(img_path)

    cur = mysql.connection.cursor()
    cur.execute("UPDATE pension SET qr_image_path = %s WHERE id = %s", (img_path,id_registro))
    mysql.connection.commit()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pension WHERE id = %s", (id_registro,))
    pension = cur.fetchone()

    return render_template('ticket_pension.html', pension=pension, os=os)

@app.route('/ticket_pagado_pension/<int:id_registro>', methods=['GET', 'POST'])
@login_required()
def ticket_pagado_pension(id_registro):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pension WHERE id = %s", (id_registro,))
    car2 = cur.fetchone()
    
    return render_template('ticket_pension.html', pension=pension, os=os)


@app.route('/descargar_pdf_pension/<int:car_id>', methods=['POST'])
@login_required()
def descargar_pdf_pension(car_id):
    cursor = mysql.connection.cursor()
    print(type(car_id))
    print({car_id})
    # Obtener registros de la base de datos
    cursor.execute('SELECT * FROM pension WHERE id = %s', (car_id, ))
    registros = cursor.fetchall()

    cursor.close()

    nombre=('registro')
    nombre2=(str(car_id))
    nombrepdf=(nombre+nombre2+'_pension.pdf')


    # Crear un PDF con la información de los registros
    pdf_path = os.path.join(os.getcwd(), nombrepdf)
    generar_pdf_pension(registros, pdf_path)

    # Enviar el PDF como respuesta para descargar
    response = make_response(send_from_directory(os.getcwd(), nombrepdf, as_attachment=True))
    return response
    
    

# Función para generar un PDF con la información de los registros
def generar_pdf_pension(registros, pdf_path):
    pdf = canvas.Canvas(pdf_path, pagesize=letter)
    pdf.setTitle("Registros")
    print(registros)

    y_position = 750
    for registro in registros:
        pdf.drawString(100, y_position, f"ID: {registro['id']}")
        pdf.drawString(100, y_position - 20, f"Placa: {registro['Placa']}")
        pdf.drawString(100, y_position - 40, f"Entrada: {registro['entry_time']}")
        pdf.drawString(100, y_position - 40, f"N.sucursal: {registro['id_sucursal']}")


        qr_image_path = registro['qr_image_path']
        if os.path.exists(qr_image_path):
            pdf.drawImage(ImageReader(qr_image_path), 100, y_position - 200, width=100, height=100)

        y_position -= 100  # Ajusta el espacio según sea necesario

    pdf.save()
    


# Ruta para editar un auto
@app.route('/editar_pension/<int:auto_id>', methods=['GET', 'POST'])
@login_required()
def editar_pension(auto_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pension WHERE id = %s", (auto_id,))
    auto = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        fecha_salida = datetime.strptime(request.form['salida'], "%Y-%m-%dT%H:%M")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE pension SET fecha_salida = %s WHERE id = %s", (fecha_salida, auto_id))
        mysql.connection.commit()
        cur.close()

        # Calcular el costo
        print(auto['fecha_entrada'])
        print(fecha_salida)
        fecha_entrada = auto['fecha_entrada']
        fecha_salida = fecha_salida
        diferencia = relativedelta(fecha_salida, fecha_entrada)

        total_meses = diferencia.years * 12 + diferencia.months
        print(total_meses)
        total_semanas = diferencia.days // 7
        total_dias = diferencia.days % 7
        
        print('tiempo',total_semanas)
        print('tiempo',total_meses)
        print('tiempo',total_dias)
        costo_dia = 200.0
        costo_semana = 1000.0
        costo_mes = 4000.0
        
        total=((total_meses*costo_mes)+(total_semanas*costo_semana)+(total_dias*costo_dia))

        
        print(total)
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE pension SET total = %s WHERE id = %s", (total, auto_id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('ticket_pension',id_registro= auto_id, os=os))

    return render_template('editar_pension.html', auto=auto)

# Ruta para eliminar un auto
@app.route('/eliminar_pension/<int:auto_id>')
@login_required()
def eliminar_pension(auto_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pension WHERE id = %s", (auto_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('pension'))

# Función para calcular el costo de pensión
def calcular_costo_pension(tiempo_estacionado_horas):
    costo_dia = 200.0
    costo_semana = 1000.0
    costo_mes = 4000.0
    print(tiempo_estacionado_horas)

    if tiempo_estacionado_horas <= 24:
        costo_total = tiempo_estacionado_horas * costo_dia
    elif tiempo_estacionado_horas <= 24 * 7:
        costo_total = costo_semana
    elif tiempo_estacionado_horas >= 24 * 30:
        costo_total = costo_mes * (tiempo_estacionado_horas // (24 * 30))
        costo_total += costo_dia * ((tiempo_estacionado_horas % (24 * 30)) / 24)

    print(costo_total)
    return costo_total



############################################################
#####################Sucursal##############################
#############################################################
@app.route('/indexsucursal')
@login_required()
def indexsucursal():
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
#----------------------------------- 
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM sucursal")
    sucursal = cur.fetchall()
    print(sucursal)
    cur.close()
    return render_template('crud_sucursal.html',sucursal=sucursal, username=username_login,id_rol=id_rol_login)

@app.route('/createsucursal')
@login_required()
def createsucursal():
    

    return render_template('create_sucursal.html')

@app.route('/addsucursal', methods=['POST'])
@login_required()
def addsucursal():
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
    descripcion = request.form['descripcion']
    codigop = request.form['codigop']
    tel = request.form['tel']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO sucursal (descripcion,codigop,telefono) VALUES (%s, %s,%s)", (descripcion, codigop,tel))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('indexsucursal'))

@app.route('/editsucursal/<int:sucursal_id>', methods=['GET', 'POST'])
@login_required()
def editsucursal(sucursal_id):
    id_login = session.get('id')
    id_rol_login = session.get('id_rol')
    id_sucursal_login = session.get('id_sucursal')
    username_login=session.get('username')
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        codigop = request.form['codigop']
        tel = request.form['tel']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE sucursal SET descripcion = %s, codigop = %s, telefono = %s WHERE id_sucursal = %s", (descripcion, codigop, tel,sucursal_id))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('indexsucursal'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM sucursal WHERE id_sucursal = %s", (sucursal_id,))
    sucursal = cur.fetchone()
    cur.close()

    return render_template('edit_sucursal.html', sucursal=sucursal, username=username_login,id_rol=id_rol_login)

@app.route('/deletesucursal/<int:sucursal_id>')
@login_required()

def deletesucursal(sucursal_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM sucursal WHERE id_sucursal = %s", (sucursal_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('indexsucursal'))

@app.route('/logout')
def logout():
    # Elimina el usuario de la sesión si está presente
    session.pop('username', None)
    return redirect(url_for('home'))

#############################################################
  
#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('home'))
    
    
    

if __name__ == '__main__':
   app.secret_key = "secretllave"
   app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
