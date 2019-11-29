let tipoOpcionTexto = null;
let tipoOpcionMultimedia = null;
let opcionesTexto = null;
let opcionesMultimedia = null;
let botonAgregarOpcion = null;
let cuentaTexto = 0;
let cuentaMultimedia = 0;

window.onload = main;

function main(){

	//obtener los elementos del DOM

	tipoOpcionTexto = document.querySelector('#opcion-texto');
	tipoOpcionMultimedia = document.querySelector('#opcion-multimedia');

	opcionesTexto = document.querySelector('.opciones-texto');
	opcionesMultimedia = document.querySelector('.opciones-multimedia');

	botonAgregarOpcion = document.querySelector('#agregar-opcion');

	//Agregando eventos

	tipoOpcionTexto.addEventListener('change', cambiarVisibilidadOpciones, true);
	tipoOpcionMultimedia.addEventListener('change', cambiarVisibilidadOpciones, true);
	botonAgregarOpcion.addEventListener('click', agregarOpcion, true);

	document.addEventListener('click', function(evento){

		let elemento = evento.target;
		let padre = elemento.parentNode;

		//Si es el boton de eliminar opcion entonces eliminamos la opcion

		if(padre.classList && padre.classList.contains('boton-eliminar-opcion')){
			let opcion = padre.parentNode;

			if(tipoOpcionTexto.checked){
				opcionesTexto.removeChild(opcion);
			}
			else{
				opcionesMultimedia.removeChild(opcion);
			}
		}

	}, true);


	document.addEventListener('change', function(evento){

		let elemento = evento.target;
		let padre = elemento.parentNode;

		//Si es el boton de eliminar opcion entonces eliminamos la opcion

		if(padre.classList.contains('opcion-multimedia')){
			leerArchivo(elemento);
		}


	}, true);

	document.addEventListener('keyup', function(evento){
		let elemento = evento.target;
		let padre = elemento.parentNode;
		
		if(padre.parentNode && padre.parentNode.classList.contains('opcion-texto')){

			let opcion = padre.parentNode;

			let radio = opcion.querySelector('input[type = "radio"]');
			console.log(elemento.value, radio)
			radio.setAttribute('value', elemento.value);
		}
	}, true);
}

function cambiarVisibilidadOpciones(){

	opcionesTexto.classList.toggle('invisible');
	opcionesMultimedia.classList.toggle('invisible');
}

function agregarOpcion(){

	//console.log(tipoOpcionTexto.checked);  true si esta activo texto
	//false si esta desactivado :v
	//Si está en opcion de texto, agregamos opcion de tipo texto
	if(tipoOpcionTexto.checked){
		agregarOpcionTexto();
	}
	else{
		agregarOpcionMultimedia();
	}
}

function agregarOpcionTexto(){

	++cuentaTexto;
	
	let htmlOpcion = `
		
		<div class="opcion-texto">
					
					<div class="input-text-fucsiaInvertido">
						<input name="opcion-texto" type="text" placeholder="Opción" required>
					</div>

					<div class="input-radio-fucsia">
						
						<input type="radio" name="opcion-correcta-texto" checked id="opcion-texto-${cuentaTexto}" value="${cuentaTexto}">
						<label for="opcion-texto-${cuentaTexto}"><span class="figura"> </span>Opción correcta</label>

					</div>

					<div class="boton-eliminar-opcion"> 
						<input type="button" value="X">
					</div>
				</div>

	`;

	let nuevaOpcion = crearElementoHTML(htmlOpcion);
	opcionesTexto.appendChild(nuevaOpcion);
}

function agregarOpcionMultimedia(){

	++cuentaMultimedia;

	let htmlOpcion = `
		
		<div class="opcion-multimedia texto-centrado">
					
					<input type="file" name="archivo-multimedia" id="archivo-multimedia-${cuentaMultimedia}" required accept="image/*, audio/*, video/*" class="invisible" >
					<label for="archivo-multimedia-${cuentaMultimedia}"> <img src="../static/img/uploads.png"> </label>
					
					<div class="input-radio-fucsia">
						
						<input type="radio" name="opcion-correcta-multimedia" checked id="opcion-multimedia-${cuentaMultimedia}" value="${cuentaMultimedia}">
						<label for="opcion-multimedia-${cuentaMultimedia}"><span class="figura"> </span>Opción correcta</label>

					</div>

					<div class="boton-eliminar-opcion"> 
						<input type="button" value="X">
					</div>

		</div>
	`;

	let nuevaOpcion = crearElementoHTML(htmlOpcion);
	opcionesMultimedia.appendChild(nuevaOpcion);


}

function leerArchivo(input){

	let lector = new FileReader();
	let padre = input.parentNode;
	let imagen = padre.querySelector('label');

	padre.removeChild(imagen);

	lector.onload = function(archivo){

		let contenido = archivo.target.result;
		let esVideo = input.files[0].type.includes("video");
		let esAudio = input.files[0].type.includes("audio");
		let esImagen = input.files[0].type.includes("image");

		let nombreArchivo = input.files[0].name;

		let opcion = input.parentNode;

		let radio = opcion.querySelector('input[type ="radio"]');
		radio.setAttribute('value', nombreArchivo);

		if(esImagen){
			agregarImagen(padre, contenido);
		}
		else if (esAudio) {
			agregarAudio(padre, contenido);
			agregarImagen(padre, '../static/img/audio.png');
		}
		else
			agregarVideo(padre, contenido);
	}

	lector.readAsDataURL(input.files[0]);
}

function agregarImagen(opcion, imagen){

	let img =  `
		<img src = "${imagen}">	
	`;

	opcion.insertBefore(crearElementoHTML(img), opcion.childNodes[0]);

}

function agregarAudio(opcion, sonido) {
	let audio = `<audio src="${sonido}" controls></audio>`;

	opcion.insertBefore(crearElementoHTML(audio), opcion.childNodes[0]);
}

function agregarVideo(opcion, video) {
	let vid = `<video src="${video}" controls></video>`;

	opcion.insertBefore(crearElementoHTML(vid), opcion.childNodes[0]);
}

function crearElementoHTML(cadenaHTML){
	let html = document.createElement('template');
	html.innerHTML = cadenaHTML;

	return html.content.cloneNode(true);
}

