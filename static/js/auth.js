// Alternar entre formulario de login y registro
function toggleForm(event) {
    event.preventDefault();
    
    const formLogin = document.getElementById('form-login');
    const formRegistro = document.getElementById('form-registro');
    const title = document.getElementById('title-login');

    if (formLogin.classList.contains('form-visible')) {
        // Cambiar a Registro
        formLogin.classList.remove('form-visible');
        formLogin.classList.add('form-hidden');
        formRegistro.classList.remove('form-hidden');
        formRegistro.classList.add('form-visible');
        title.textContent = 'Regístrate';
    } else {
        // Cambiar a Login
        formRegistro.classList.remove('form-visible');
        formRegistro.classList.add('form-hidden');
        formLogin.classList.remove('form-hidden');
        formLogin.classList.add('form-visible');
        title.textContent = 'Inicia Sesión';
    }
}

// Manejar envío de formularios
document.getElementById('form-login').addEventListener('submit', function(e) {
    e.preventDefault();
    console.log('Login enviado');
    // Aquí irá la lógica para enviar datos al servidor
});

document.getElementById('form-registro').addEventListener('submit', function(e) {
    e.preventDefault();
    console.log('Registro enviado');
    // Aquí irá la lógica para enviar datos al servidor
});

