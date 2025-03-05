document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ Script cargado correctamente");

    const btnAgregar = document.getElementById("btn-agregar");
    const nombreProducto = document.getElementById("nombre-producto");
    const precioProducto = document.getElementById("precio");
    const localidad = document.getElementById("localidad");
    const tablaProductosBody = document.getElementById("tabla-productos-body");

    function cargarProductosRecientes() {
        console.log("📡 Cargando productos recientes...");

        fetch("/api/productos-hoy/")
            .then(response => {
                console.log("📬 Respuesta recibida de productos recientes:", response);
                return response.json();
            })
            .then(data => {
                console.log("📂 Productos recibidos:", data.productos);
                tablaProductosBody.innerHTML = ""; 

                if (data.productos.length === 0) {
                    console.warn("⚠️ No hay productos recientes.");
                    tablaProductosBody.innerHTML = "<tr><td colspan='4' style='text-align:center;'>No hay productos recientes.</td></tr>";
                    return;
                }

                data.productos.forEach(producto => {
                    const fila = `
                        <tr>
                            <td>${producto.name}</td>
                            <td>$${producto.precio.toFixed(2)}</td>
                            <td>${producto.localidad}</td>
                            <td><button class="boton-eliminar" data-id="${producto.id}">Eliminar</button></td>
                        </tr>
                    `;
                    tablaProductosBody.innerHTML += fila;
                });

                document.querySelectorAll(".boton-eliminar").forEach(button => {
                    button.addEventListener("click", eliminarProducto);
                });
            })
            .catch(error => console.error("❌ Error cargando productos recientes:", error));
    }

    btnAgregar.addEventListener("click", () => {
        console.log("🆕 Intentando agregar nuevo producto...");

        const nombre = nombreProducto.value.trim();
        const precio = parseFloat(precioProducto.value);
        const localidadID = localidad.value;

        console.log("🔹 Datos recopilados:", { nombre, precio, localidadID });

        if (!nombre || isNaN(precio) || precio <= 0 || !localidadID) {
            alert("❌ Todos los campos son obligatorios y el precio debe ser mayor a 0.");
            return;
        }

        const productoData = {
            nombre: nombre,
            precio: precio,
            localidad_id: localidadID
        };

        console.log("📤 Enviando datos al servidor:", productoData);

        fetch("/api/agregar-producto/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(productoData)
        })
        .then(response => {
            console.log("📬 Respuesta del servidor:", response);
            return response.json();
        })
        .then(data => {
            if (data.success) {
                console.log("✅ Producto agregado correctamente.");
                alert("Producto agregado correctamente.");
                cargarProductosRecientes(); 
                nombreProducto.value = "";
                precioProducto.value = "";
                localidad.value = "";
            } else {
                console.error("❌ Error:", data.message);
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => console.error("❌ Error al enviar datos:", error));
    });

    function eliminarProducto(event) {
        const productoID = event.target.getAttribute("data-id");
        console.log(`🗑 Eliminando producto con ID: ${productoID}`);

        fetch(`/api/eliminar-producto/${productoID}/`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("✅ Producto eliminado correctamente.");
                alert("Producto eliminado correctamente.");
                cargarProductosRecientes();
            } else {
                console.error("❌ Error eliminando producto:", data.message);
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => console.error("❌ Error al eliminar producto:", error));
    }

    cargarProductosRecientes(); 
});