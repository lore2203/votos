// Espera a que el contenido de la página esté cargado
document.addEventListener('DOMContentLoaded', () => {

    // Selecciona los elementos del DOM
    const form = document.getElementById('voter-form');
    const resultContainer = document.getElementById('result-container');
    const candidateEl = document.getElementById('result-candidate');
    const confidenceEl = document.getElementById('result-confidence');
    const submitBtn = document.getElementById('submit-btn');

    // URL del backend. 
    // Usamos 'localhost:5000' porque Docker Compose conectará el puerto.
    const API_URL = 'http://backend:5000/predict';

    // Escucha el evento 'submit' del formulario
    form.addEventListener('submit', async (e) => {
        // Previene que la página se recargue
        e.preventDefault();

        // Deshabilitar el botón para evitar envíos múltiples
        submitBtn.disabled = true;
        submitBtn.textContent = 'Procesando...';
        resultContainer.classList.add('hidden');

        // 1. Recoger los datos del formulario
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            // 2. Enviar los datos al Backend (API)
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                // Si el servidor responde con un error
                throw new Error(`Error del servidor: ${response.statusText}`);
            }

            // 3. Recibir la respuesta JSON del backend
            const result = await response.json();

            // 4. Mostrar los resultados
            candidateEl.textContent = result.candidato_predicho;
            confidenceEl.textContent = `${result.probabilidad}%`;
            resultContainer.classList.remove('hidden');

        } catch (error) {
            // Manejar errores de red o del fetch
            console.error('Error al contactar la API:', error);
            candidateEl.textContent = 'Error';
            confidenceEl.textContent = 'No se pudo obtener predicción. Revisa la consola.';
            resultContainer.classList.remove('hidden');
        } finally {
            // Volver a habilitar el botón
            submitBtn.disabled = false;
            submitBtn.textContent = 'Predecir Afinidad';
        }
    });
});