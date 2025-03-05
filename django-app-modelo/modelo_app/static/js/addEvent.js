document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ Script cargado correctamente");

    const btnAgregar = document.getElementById("btn-agregar");
    const nombreEvento = document.getElementById("nombre-evento");
    const fechaInicio = document.getElementById("fecha-inicio");
    const fechaFin = document.getElementById("fecha-fin");
    const localidad = document.getElementById("localidad");
    const imagenUrl = document.getElementById("imagen-url");
    const tablaEventosBody = document.getElementById("tabla-eventos-body");

    function cargarEventosRecientes() {
        console.log("📡 Cargando eventos recientes...");

        fetch("/api/eventos-hoy/")
            .then(response => response.json())
            .then(data => {
                console.log("📂 Eventos recibidos:", data.eventos);
                tablaEventosBody.innerHTML = ""; 

                if (data.eventos.length === 0) {
                    console.warn("⚠️ No hay eventos recientes.");
                    tablaEventosBody.innerHTML = "<tr><td colspan='5' style='text-align:center;'>No hay eventos recientes.</td></tr>";
                    return;
                }

                data.eventos.forEach(evento => {
                    const fila = document.createElement("tr");
                    fila.innerHTML = `
                        <td>${evento.name}</td>
                        <td>${evento.fecha_inicio}</td>
                        <td>${evento.fecha_fin}</td>
                        <td>${evento.localidad}</td>
                        <td>
                            <button class="boton-eliminar" data-id="${evento.id}">Eliminar</button>
                        </td>
                    `;
                    tablaEventosBody.appendChild(fila);
                });

                document.querySelectorAll(".boton-eliminar").forEach(boton => {
                    boton.addEventListener("click", eliminarEvento);
                });
            })
            .catch(error => console.error("❌ Error cargando eventos recientes:", error));
    }

    function agregarEvento() {
        console.log("🆕 Intentando agregar nuevo evento...");

        const nombre = nombreEvento.value.trim();
        const inicio = fechaInicio.value;
        const fin = fechaFin.value;
        const localidadID = localidad.value;
        const imagen = imagenUrl.value.trim();

        console.log("🔹 Datos recopilados:", { nombre, inicio, fin, localidadID, imagen });

        if (!nombre || !inicio || !fin || !localidadID || !imagen) {
            alert("❌ Todos los campos son obligatorios.");
            return;
        }

        const eventoData = {
            nombre: nombre,
            fechaInicio: inicio,
            fechaFin: fin,
            localidad_id: localidadID,
            imagen_url: imagen
        };

        console.log("📤 Enviando datos al servidor:", eventoData);

        fetch("/api/agregar-evento/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(eventoData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("✅ Evento agregado correctamente.");
                alert("Evento agregado correctamente.");
                limpiarFormulario();
                cargarEventosRecientes();
            } else {
                console.error("❌ Error:", data.message);
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => console.error("❌ Error al enviar datos:", error));
    }

    function eliminarEvento(event) {
        const eventoID = event.target.getAttribute("data-id");
        console.log(`🗑️ Intentando eliminar evento ID: ${eventoID}`);

        if (!confirm("¿Estás seguro de que deseas eliminar este evento?")) {
            return;
        }

        fetch(`/api/eliminar-evento/${eventoID}/`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log(`✅ Evento ${eventoID} eliminado correctamente.`);
                alert("Evento eliminado correctamente.");
                cargarEventosRecientes();
            } else {
                console.error("❌ Error eliminando evento:", data.message);
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => console.error("❌ Error en la solicitud de eliminación:", error));
    }

    function limpiarFormulario() {
        nombreEvento.value = "";
        fechaInicio.value = "";
        fechaFin.value = "";
        localidad.value = "";
        imagenUrl.value = "";
    }

    btnAgregar.addEventListener("click", agregarEvento);
    cargarEventosRecientes();
});