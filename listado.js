const URL = "https://sofitarabusi.pythonanywhere.com" // Realizamos la solicitud GET al servidor para obtener todos los productos 

fetch(URL + '/cliente')
    .then(function (response) {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error al obtener los productos')
        }
    })
    .then(function (data) {
        let tablaClientes = document.getElementById('tablaClientes')
        //iteramos sobre los productos y agregamos filas a la tabla
        for (let cliente of data) {
            let fila = document.createElement('tr');
            fila.innerHTML = '<td>' + cliente.idclientes + '</td>' + '<td>' + cliente.nombre + '</td>' + '<td align="right">' + cliente.apellido + '</td>' + '<td align="right">' + cliente.telefono + '</td>' + '<td>' + cliente.localidad + '<td align="right">' + cliente.direccion + '</td>' + '<td align="right">' + cliente.bolson + '</td>' + '<td align="right">' + cliente.medio_de_pago + '</td>' + '<td align="right">' + cliente.dia_de_entrega + '</td>' + '<td>' + '<button @click="eliminarCliente(cliente.idclientes)">Eliminar</button>' + '<a type="button" href="../PROYECTO-API/modificaciones.html">Modificar</a>' + '</td>';

            //cambio  + '<button @click="modificarCliente(cliente.idcliente)">Editar</button>' + '</td>' por un enlace a: que me lleve a la página modificaciones.html pero con esto se le va la formita de botón como tiene eliminar.. 
            //EN REALIDAD ESTO NO ALCANZA!!!!! PORQUE TENDRIA QUE INGRESAR MANUALMENTE EL ID PARA EDITARLO Y NO QUIERO QUE SEA ASI SINO DARLE MODIFICAR Y QUE YA IMPORTE LA "FICHA" CON LOS DATOS DE ESE IDCLIENTES Y PODER MODIFICARLA, ASI QUE DEBERÍA HACER UNA FUNCIÓN EN JS QUE CUANDO DE CLICK HAGA CIERTAS COSAS

            //una vez que se crea la fila con el contenido del producto se agrega a la tabla usando el metodo appendChild del elemento tablaProductos
            tablaClientes.appendChild(fila);
        }
    });

//Esto estaba en el código pero hacia que en la primer carga de listado.html saltara ese mensaje y tuviera que recargar para obtener el listado sin el mensaje!!!! 
// .catch(function(error){
//     alert('Error al agregar el cliente.');
//     console.error('Error:', error)
// })    


// ACÁ MISMO DEBERÍA AGREGAR LA FUNCIONALIDAD DEL BOTÓN ELIMINAR ... Y MODIFICAR SERÍA UN LINK A LA PÁGINA MODIFICAR??


const app = Vue.createApp({
    data() {
        return {
            clientes: []  // Inicializar un array para almacenar los clientes
        };
    },

    methods: {
        eliminarCliente(idclientes) {
            if (confirm('¿Estás seguro que quieres eliminar este cliente?')) {
                fetch(URL + 'clientes/$(idclientes)', { method: 'DELETE' })
                    .then(response => {
                        this.clientes = this.clientes.filter(clientes => cliente.idclientes !== idclientes);
                        alert('Cliente eliminado correctamente.');
                    })
                    .catch(error => {
                        alert(error.message);
                    });

            }
        }
    },

});
app.mount('body');