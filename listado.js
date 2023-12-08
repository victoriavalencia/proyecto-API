const URL = "https://sofitarabusi.pythonanywhere.com" // Realizamos la solicitud GET al servidor para obtener todos los productos 
fetch(URL + '/cliente')
    .then(function (response) {
        if (response.ok) {
             return response.json();
        } else {
            throw new Error ('Error al obtener los productos')
        }
    })
    .then(function(data){
        let tablaClientes = document.getElementById('tablaClientes')
        //iteramos sobre los productos y agregamos filas a la tabla
        for (let cliente of data){
            let fila = document.createElement('tr');
            fila.innerHTML ='<td>' + cliente.idclientes+ '</td>' + '<td>' + cliente.nombre + '</td>' + '<td align="right">' + cliente.apellido + '</td>' + '<td align="right">' + cliente.telefono + '</td>' + '<td>' + cliente.localidad + '<td align="right">' + cliente.direccion + '</td>' + '<td align="right">' + cliente.bolson + '</td>' + '<td align="right">' + cliente.medio_de_pago + '</td>' + '<td align="right">' + cliente.dia_de_entrega + '</td>' + '<td>' + '<button @click="eliminarCliente(producto.codigo)">Eliminar</button>' + '<button @click="modificarCliente(producto.codigo)">Editar</button>' + '</td>';

            //una vez que se crea la fila con el contenido del producto se agrega a la tabla usando el metodo appendChild del elemento tablaProductos
            tablaClientes.appendChild(fila);
        }
    })

    //Esto estaba en el código pero hacia que en la primer carga de listado.html saltara ese mensaje y tuviera que recargar para obtener el listado sin el mensaje!!!! 
    // .catch(function(error){
    //     alert('Error al agregar el cliente.');
    //     console.error('Error:', error)
    // })    