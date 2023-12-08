const URL = "https://sofitarabusi.pythonanywhere.com" //En el pdf usan el http://127.0.0.1:500 que es el servidor local, ahora que está en py anywhere qué url debería ser?? 

//capturamos el evento de envio del formulario 
document.getElementById('formulario').addEventListener('submit',function(event) {
    event.preventDefault(); //evitamos que se envie el form 

    var formData = new FormData(); //creo el objeto FormData para enviar datos de formulario al servidor. 

    //con el método .append agrego al objeto formData los datos en formato clave:valor 'nombre' es la clave y el valor se obtiene del elemento html con el id 'nombre'
    formData.append('nombre', document.getElementById('nombre').value); //'va el ID'
    formData.append('apellido', document.getElementById('apellido').value); 
    formData.append('telefono', document.getElementById('telefono').value); 
    formData.append('localidad', document.getElementById('localidad').value); 
    formData.append('direccion', document.getElementById('direccion').value); 
    formData.append('bolson', document.getElementById('bolson_numero').value);
    formData.append('medio_de_pago', document.getElementById('medio_de_pago').value);
    formData.append('dia_de_entrega', document.getElementById('dia_de_entrega').value);

    //ahora realizamos la solicitud POST al servidor.
    fetch (URL + 'productos', {method: 'POST', body: formData}) 

    //luego usamos el método then () para manejar la respuesta del servidor. Si es exitosa, .ok, convierte los datos de la respuesta a formato JSON, sino la palabra throw se usa para lanzar una instancia de la clase Error con un mensaje específico. 
    .then(function(response) {
        if (response.ok){
            return response.json();
        }else {
            throw new Error('Error al agregar el cliente.');
        }
    })

    //Si fue exitoso el registro muestra un mensaje 
    .then(function(){
        alert('Cliente agregado correctamente');
    }) 

    //catch muestra alerta de error como pop-up y en la consola si hay error durante la solicitud fetch
    .catch(function(error){
        alert('Error al agregar el cliente.');
        console.error('Error:', error)
    })

    //para limpiar el formulario en ámbos casos exito o error:
    .finally(function(){
        document.getElementById('nombre').value ="";
        document.getElementById('apellido').value ="";
        document.getElementById('telefono').value ="";
        document.getElementById('localidad').value ="";
        document.getElementById('direccion').value ="";
        document.getElementById('bolson_numero').value ="";
        document.getElementById('medio_de_pago').value ="";
        document.getElementById('dia_de_entrega').value ="";
    });


})