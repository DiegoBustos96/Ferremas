// static/js/main.js
console.log("FERREMAS JS Cargado");

// Puedes añadir aquí interacciones generales si las necesitas
// Por ejemplo, validaciones de formulario adicionales, efectos visuales, etc.

// Ejemplo: Cerrar alertas de mensajes automáticamente después de unos segundos
document.addEventListener('DOMContentLoaded', (event) => {
    const alerts = document.querySelectorAll('.alert.alert-dismissible');
    alerts.forEach(function(alert) {
        // No cerrar errores persistentes
        if (!alert.classList.contains('alert-danger') && !alert.classList.contains('alert-warning')) {
             setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000); // Cerrar después de 5 segundos
        }
    });
});