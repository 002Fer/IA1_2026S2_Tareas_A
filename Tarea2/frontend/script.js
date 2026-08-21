
const URL_API = "http://127.0.0.1:8000/inventario";

const formulario = document.getElementById("formularioBusqueda");

const inputItem = document.getElementById("item");

const mensaje = document.getElementById("mensaje");

const resultados = document.getElementById("resultados");

const itemBuscado = document.getElementById("itemBuscado");

const totalItems = document.getElementById("totalItems");

const inventarioInvertido = document.getElementById(
    "inventarioInvertido"
);

const inventarioUnico = document.getElementById(
    "inventarioUnico"
);

const inventarioOrdenado = document.getElementById(
    "inventarioOrdenado"
);


formulario.addEventListener("submit", async function (evento) {

    evento.preventDefault();

    const item = inputItem.value.trim();

    mensaje.textContent = "";

    resultados.classList.add("oculto");


    if (item === "") {

        mensaje.textContent = "Debe ingresar un item.";

        mensaje.className = "mensaje error";

        return;
    }

    try {

        mensaje.textContent = "Consultando inventario...";

        mensaje.className = "mensaje";



        const respuesta = await fetch(
            `${URL_API}?item=${encodeURIComponent(item)}`
        );


        const datos = await respuesta.json();



        if (!respuesta.ok) {

            throw new Error(
                datos.detail || "No se pudo realizar la consulta."
            );

        }

        itemBuscado.textContent =
            datos.item_buscado;

        totalItems.textContent =
            datos.total_items;

        inventarioInvertido.textContent =
            mostrarLista(datos.inventario_invertido);

        inventarioUnico.textContent =
            mostrarLista(datos.inventario_unico);

        inventarioOrdenado.textContent =
            mostrarLista(datos.inventario_ordenado);


        resultados.classList.remove("oculto");


        mensaje.textContent =
            "Consulta realizada correctamente.";

        mensaje.className =
            "mensaje exito";
    }

    catch (error) {

        mensaje.textContent = error.message;

        mensaje.className =
            "mensaje error";

        resultados.classList.add("oculto");
    }

});

function mostrarLista(lista) {

    return lista.join(", ");

}