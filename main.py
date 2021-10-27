from flask import Flask, render_template, request,flash, session, redirect
import sqlite3
import os

from werkzeug.utils import escape

from forms.formularios import Login, Productos, Registro
import hashlib

app = Flask(__name__)

app.secret_key = os.urandom(20)

@app.route("/", methods=["GET", "POST"])
def home():
    frm = Login()
    if frm.validate_on_submit():
        username = escape(frm.username.data)
        password = escape(frm.password.data)
        # Cifra la contraseña
        encrp = hashlib.sha256(password.encode('utf-8'))
        pass_enc = encrp.hexdigest()
        with sqlite3.connect("vacunacion.db") as con:
            con.row_factory = sqlite3.Row  # Lista de diccionario
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM usuario WHERE username = ? AND password =?", [username, pass_enc])
            # cur.execute("SELECT * FROM usuario WHERE username = '" +
            #             username + "' AND password ='" + pass_enc + "'")
            row = cur.fetchone()
            if row:
                session["usuario"] = username
                session["perfil"] = row["perfil"]
                if row["perfil"] == 1:
                    return "Hola, ADMIN"
                elif row["perfil"] == 2:
                    return redirect("/productos")
            else:
                return "Usuario/Password incorrectos"

    return render_template("login.html", frm=frm)


# API para registrar los Usuarios
@app.route("/registro", methods=["GET", "POST"])
def registrar():
    frm = Registro()
    if frm.validate_on_submit():
        if frm.enviar:
            username = frm.username.data
            correo = frm.correo.data
            nombre = frm.nombre.data
            password = frm.password.data
            # Cifra la contraseña
            encrp = hashlib.sha256(password.encode('utf-8'))
            pass_enc = encrp.hexdigest()
            # Conecta a la BD
            with sqlite3.connect("vacunacion.db") as con:
                # Crea un cursor para manipular la BD
                cur = con.cursor()
                # Prepara la sentencia SQL
                cur.execute("INSERT INTO usuario (nombre, username, correo, password) VALUES (?,?,?,?)", [
                            nombre, username, correo, pass_enc])
                # Ejecuta la sentencia SQL
                con.commit()
                return "Guardado con éxito <a href='/'>Home</a>"

    return render_template("registro.html", frm=frm)


@app.route("/usuario/listar", methods=["GET", "POST"])
def usuario_listar():
    with sqlite3.connect("vacunacion.db") as con:
        con.row_factory = sqlite3.Row  # Lista de diccionario
        cur = con.cursor()
        cur.execute("SELECT * FROM usuario")

        rows = cur.fetchall()

        return render_template("lista-usuarios.html", rows=rows)


@app.route("/usuario/eliminar", methods=["GET", "POST"])
def usuario_eliminar():
    frm = Registro()
    if request.method == "POST":
        username = frm.username.data
        with sqlite3.connect("vacunacion.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM usuario WHERE username = ?", [username])
            con.commit()

            return "Usuario eliminado"
    return render_template("eliminar-usuario.html", frm=frm)


@app.route("/productos")
def productos():
    # Verifica si esta logeado
    if "usuario" in session:
    #if "usuario" in session and session["perfil"] == 2: #Excepciones de funciones a usuarios
        frm = Productos()
        username = session["usuario"]
        return render_template("productos.html", frm=frm, username = username)
    else:
        return redirect("/")


@app.route("/producto/save", methods = ["POST"])
def prod_save():
    frm = Productos()
    nombre = frm.nombre.data
    precio = frm.precio.data
    stock = frm.stock.data
    if len(nombre) > 0:
        if len(precio) > 0:
            if len(stock) > 0:
                with sqlite3.connect("vacunacion.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO productos (nombre,precio,stock) VALUES (?,?,?)", [
                                nombre, precio, stock])
                    con.commit()
                    flash("Guardado con éxito")
            else:
                flash("ERROR: Stock es requerido")
        else:
            flash("ERROR: Precio es requerido")
    else:
        flash("ERROR: Nombre es requerido")

    return render_template("productos.html", frm=frm)


@app.route("/producto/get", methods=["POST"])
def prod_get():
    frm = Productos()
    codigo = frm.codigo.data
    if len(codigo) > 0:
        with sqlite3.connect("vacunacion.db") as con:
             con.row_factory = sqlite3.Row  # Lista de diccionario
             cur = con.cursor()
             cur.execute("SELECT * FROM productos WHERE codigo = ?",[codigo])
             row = cur.fetchone()
             if row:
                 frm.nombre.data = row["nombre"]
                 frm.precio.data = row["precio"]
                 frm.stock.data = row["stock"]
                 
             else:
                 frm.nombre.data = ""
                 frm.precio.data = ""
                 frm.stock.data = ""
                 flash("Producto No encontrado")
                
    return render_template("productos.html", frm = frm)

@app.route("/producto/delete", methods=["POST"])
def prod_delete():
    frm = Productos()
    #escape sirve para limpiar el dato contra instrucciones malisiosas
    codigo = escape(frm.codigo.data)
    if codigo:
        with sqlite3.connect("vacunacion.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM productos WHERE codigo = ?", [codigo])
            con.commit()
            if con.total_changes > 0:
                flash("Producto Eliminado")
            else:
                flash("Producto No se pudo Eliminar")
                
    return render_template("productos.html", frm=frm)
            
            

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


app.run(debug=True)
