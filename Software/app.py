from flask import Flask, render_template, request, redirect, flash
import xml.etree.ElementTree as arbolXml
from xml.dom import minidom
from lxml import etree
import hashlib 

#creamos el servidor
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

RUTA_PREGUNTAS = './static/preguntas/preguntas.xml'

@app.route('/') #le dice al servidor que hacer cuando recibe una peticion en esa dirección

def index():
	# isaac = "amor"
	# mensaje = f"<h1>hola {isaac}"

	#obtener la informacion de las preguntas

	etiquetaPreguntas = minidom.parse(RUTA_PREGUNTAS)
	informacionPreguntas = etiquetaPreguntas.getElementsByTagName('informacionPregunta')

	nombreIdPreguntas = []

	#Obteniendo informacion de las preguntas
	for i in range(len(informacionPreguntas)):
		etiquetaNombre = informacionPreguntas[i].getElementsByTagName('nombre')[0]
		nombre = etiquetaNombre.firstChild.nodeValue

		idPregunta = informacionPreguntas[i].attributes['id'].value

		pregunta = (nombre, idPregunta)
		nombreIdPreguntas.append(pregunta)

		print(pregunta)

	return render_template('index.html', infoPreguntas = nombreIdPreguntas)




@app.route('/creacionPregunta')

def creacionPregunta():
	return render_template('creacionPreguntas.html')





def formatoXML(nombreArchivo):
	convertidor = etree.XMLParser(resolve_entities = False, strip_cdata = False)
	documento = etree.parse(nombreArchivo, convertidor)
	documento.write(nombreArchivo, pretty_print = True, encoding = 'utf-8')

def hashCadena( cadena):
	idhash = hashlib.md5(cadena.encode('utf-8'))
	return idhash.hexdigest()

def guardarPreguntaTexto(nombre, pregunta, listaOpciones, opcionCorrecta):

	#para crear las etiquetas que guardaremos en el xml

	etiquetaInformacionPregunta = arbolXml.Element('informacionPregunta')
	etiquetaNombre = arbolXml.SubElement(etiquetaInformacionPregunta, 'nombre')
	etiquetaPregunta = arbolXml.SubElement(etiquetaInformacionPregunta, 'pregunta')
	etiquetaTipo = arbolXml.SubElement(etiquetaInformacionPregunta, 'tipo')
	etiquetaOpciones= arbolXml.SubElement(etiquetaInformacionPregunta, 'opciones')
	etiquetaOpcionCorrecta= arbolXml.SubElement(etiquetaInformacionPregunta, 'opcionCorrecta')

	#para modificar el "valor" de lo que hay entre las etiquetas:

	etiquetaNombre.text = nombre
	etiquetaPregunta.text = pregunta
	etiquetaTipo.text = "texto"
	etiquetaOpcionCorrecta.text = opcionCorrecta

	etiquetaInformacionPregunta.set('id', hashCadena(nombre))

	for i in range(len(listaOpciones)):
		etiquetaOpcion = arbolXml.SubElement(etiquetaOpciones, 'opcion')
		etiquetaOpcion.text = listaOpciones[i]


	preguntas = arbolXml.parse(RUTA_PREGUNTAS).getroot()

	preguntas.append(etiquetaInformacionPregunta)
	informacionPreguntas = arbolXml.ElementTree(preguntas)
	informacionPreguntas.write(RUTA_PREGUNTAS)
	#para prepararlo para guardarlo en un archivo

	formatoXML(RUTA_PREGUNTAS)


def guardarPreguntaMultimedia(nombre, pregunta, archivos, opcionCorrecta):
	#para crear las etiquetas que guardaremos en el xml

	etiquetaInformacionPregunta = arbolXml.Element('informacionPregunta')
	etiquetaNombre = arbolXml.SubElement(etiquetaInformacionPregunta, 'nombre')
	etiquetaPregunta = arbolXml.SubElement(etiquetaInformacionPregunta, 'pregunta')
	etiquetaTipo = arbolXml.SubElement(etiquetaInformacionPregunta, 'tipo')
	etiquetaOpciones= arbolXml.SubElement(etiquetaInformacionPregunta, 'opciones')
	etiquetaOpcionCorrecta= arbolXml.SubElement(etiquetaInformacionPregunta, 'opcionCorrecta')

	#para modificar el "valor" de lo que hay entre las etiquetas:

	etiquetaNombre.text = nombre
	etiquetaPregunta.text = pregunta
	etiquetaTipo.text = "multimedia"

	idPregunta = hashCadena(nombre)
	etiquetaOpcionCorrecta.text = idPregunta + opcionCorrecta


	etiquetaInformacionPregunta.set('id', idPregunta)

	for i in range(len(archivos)):
		etiquetaOpcion = arbolXml.SubElement(etiquetaOpciones, 'opcion')
		nuevoNombre = idPregunta + archivos[i].filename
		etiquetaOpcion.text = nuevoNombre

		archivos[i].save(f"static/preguntas/{nuevoNombre}")

	preguntas = arbolXml.parse(RUTA_PREGUNTAS).getroot()

	preguntas.append(etiquetaInformacionPregunta)
	informacionPreguntas = arbolXml.ElementTree(preguntas)
	informacionPreguntas.write(RUTA_PREGUNTAS)
	#para prepararlo para guardarlo en un archivo

	formatoXML(RUTA_PREGUNTAS)

	return 

@app.route('/crearPregunta', methods = ['POST'])

def crearPregunta():

	if request.method == 'POST':

		if request.form.get('nombre') == None or request.form.get('tipo-opcion') == None or (request.form.get('opcion-correcta-texto') == None and request.form.get('opcion-correcta-multimedia') == None):
			flash('No se llenaron todos los campos')
			return redirect('/creacionPregunta')

		nombre = request.form['nombre']
		pregunta = request.form['pregunta']
		tipoOpcion = request.form['tipo-opcion']
		listaOpciones = []


		if len(nombre.replace(' ', '')) == 0 or len(pregunta.replace(' ', '')) == 0 or len(tipoOpcion.replace(' ', '')) == 0:
			flash('No se llenaron todos los campos')
			return redirect('/creacionPregunta')

		#Sí es de opcion texto

		if tipoOpcion == '1':
			listaOpciones = request.form.getlist('opcion-texto')
			opcionCorrectaTexto = request.form['opcion-correcta-texto']

			if len(listaOpciones) <= 1:
				flash('No hay suficientes opciones')
				return redirect('/creacionPregunta')

			for opcion in listaOpciones:
				if len(opcion.replace(' ', '')) == 0:
					flash('Hay opciones vacías')
					return redirect('/creacionPregunta')


			guardarPreguntaTexto(nombre, pregunta, listaOpciones, opcionCorrectaTexto)



		else:

			archivos = request.files.getlist('archivo-multimedia')
			opcionCorrectaMultimedia = request.form['opcion-correcta-multimedia']


			if archivos <= 1:
				flash('No hay suficientes opciones')
				return redirect('/creacionPregunta')

			guardarPreguntaMultimedia(nombre, pregunta, archivos, opcionCorrectaMultimedia)
			

	return redirect('/')

#para acceder a la pregunta con su id
@app.route('/verPregunta/<idPregunta>')
def verPregunta(idPregunta):
	
	etiquetaPreguntas =  minidom.parse(RUTA_PREGUNTAS)
	informacionPregunta = None

	for pregunta in etiquetaPreguntas.getElementsByTagName('informacionPregunta'):

		if(pregunta.attributes['id'].value == idPregunta):
			informacionPregunta = pregunta
			break

	if informacionPregunta != None:

		nombre = informacionPregunta.getElementsByTagName('nombre')[0].firstChild.nodeValue
		pregunta = informacionPregunta.getElementsByTagName('pregunta')[0].firstChild.nodeValue
		tipo = informacionPregunta.getElementsByTagName('tipo')[0].firstChild.nodeValue
		etiquetaOpciones = informacionPregunta.getElementsByTagName('opciones')[0]
		opcionCorrecta = informacionPregunta.getElementsByTagName('opcionCorrecta')[0].firstChild.nodeValue

		opciones = []

		for etiquetaOpcion in etiquetaOpciones.getElementsByTagName('opcion'):
			opciones.append(etiquetaOpcion.firstChild.nodeValue)


	return render_template('verPregunta.html', nombre = nombre, pregunta = pregunta, tipo = tipo, opciones = opciones, opcionCorrecta = opcionCorrecta)


def eliminarPorId(idPregunta):
	root = arbolXml.parse(RUTA_PREGUNTAS).getroot()
	preguntas = root.getchildren()

	for pregunta in preguntas:
		if pregunta.attrib['id'] == idPregunta:
			root.remove(pregunta)


	informacionPreguntas = arbolXml.ElementTree(root)

	informacionPreguntas.write(RUTA_PREGUNTAS)


@app.route('/eliminar/<idPregunta>')

def eliminarPregunta(idPregunta):
	
	eliminarPorId(idPregunta)

	return redirect('/')

@app.route('/editarPregunta/<idPregunta>')
def editarPregunta(idPregunta):

	etiquetaPreguntas = minidom.parse(RUTA_PREGUNTAS)
	informacionPreguntas = etiquetaPreguntas.getElementsByTagName('informacionPregunta')

	etiquetaPregunta = None

	for i in range( len(informacionPreguntas)):
		if informacionPreguntas[i].attributes['id'].value == idPregunta:
			etiquetaPregunta = informacionPreguntas[i]
			break

	nombre = etiquetaPregunta.getElementsByTagName('nombre')[0].firstChild.nodeValue
	pregunta = etiquetaPregunta.getElementsByTagName('pregunta')[0].firstChild.nodeValue
	tipo = etiquetaPregunta.getElementsByTagName('tipo')[0].firstChild.nodeValue
	opcionCorrecta = etiquetaPregunta.getElementsByTagName('opcionCorrecta')[0].firstChild.nodeValue
	etiquetaOpcion = etiquetaPregunta.getElementsByTagName('opcion')

	opciones = []



	for i in range( len(etiquetaOpcion)):
		opciones.append(etiquetaOpcion[i].firstChild.nodeValue)
	
	return render_template('editarPregunta.html', nombre = nombre, pregunta = pregunta, tipo = tipo, opcionCorrecta = opcionCorrecta, opciones = opciones, idPregunta = idPregunta)

@app.route('/editar/<idPregunta>', methods = ['POST'])

def editar(idPregunta):

	if request.method == 'POST':

		if request.form.get('nombre') == None or request.form.get('tipo-opcion') == None or (request.form.get('opcion-correcta-texto') == None and request.form.get('opcion-correcta-multimedia') == None):
			flash('No se llenaron todos los campos')
			return redirect('/editarPregunta/' + idPregunta)

		nombre = request.form['nombre']
		pregunta = request.form['pregunta']
		tipoOpcion = request.form['tipo-opcion']
		listaOpciones = []

		if len(nombre.replace(' ', '')) == 0 or len(pregunta.replace(' ', '')) == 0 or len(tipoOpcion.replace(' ', '')) == 0:
			flash('No se llenaron todos los campos')
			return redirect('/editarPregunta/' + idPregunta)

		#Sí es de opcion texto

		if tipoOpcion == '1':

			listaOpciones = request.form.getlist('opcion-texto')
			opcionCorrectaTexto = request.form['opcion-correcta-texto']

			if len(listaOpciones) <= 1:
				flash('No hay suficientes opciones')
				return redirect('/editarPregunta/' + idPregunta)
	
			eliminarPorId(idPregunta)
			guardarPreguntaTexto(nombre, pregunta, listaOpciones, opcionCorrectaTexto)

		else:

			archivos = request.files.getlist('archivo-multimedia')
			opcionCorrectaMultimedia = request.form['opcion-correcta-multimedia']

			if archivos <= 1:
				flash('No hay suficientes opciones')
				return redirect('/editarPregunta/' + idPregunta)

			guardarPreguntaMultimedia(nombre, pregunta, archivos, opcionCorrectaMultimedia)
			eliminarPorId(idPregunta)
			

	return redirect('/')


#Definir el main
if __name__ == '__main__':
	#regresamos el objeto de la aplicacion
	app.run( port = 3000, debug = True)  #Debug para no estar reiniciando el servidor

