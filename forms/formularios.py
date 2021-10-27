from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired

class Registro(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    nombre = StringField("Nombre", validators=[DataRequired()])
    correo = StringField("Correo", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    enviar = SubmitField("Registrar")
    editar = SubmitField("Editar")
    eliminar = SubmitField("Eliminar")
    consultar = SubmitField("Eliminar")

class Login(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    entrar = SubmitField("Entrar") 


class Productos(FlaskForm):
    codigo = StringField("Código")
    nombre = StringField("Nombre")
    precio = StringField("Precio")
    stock = StringField("Stock")
    guardar = SubmitField("Guardar", render_kw=({"onfocus":"cambiaRuta('/producto/save')"}))
    consultar = SubmitField("Consultar", render_kw=({"onfocus":"cambiaRuta('/producto/get')"}))
    editar = SubmitField("Editar", render_kw=({"onfocus":"cambiaRuta('/producto/update')"}))
    eliminar = SubmitField("Eliminar", render_kw=({"onfocus":"cambiaRuta('/producto/delete')"}))