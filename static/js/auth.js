// ============== NAVEGACIÓN MÓVIL ==============
document.addEventListener('DOMContentLoaded', function() {
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            navLinks?.classList.toggle('active');
            
            // Animar los spans del toggle
            const spans = this.querySelectorAll('span');
            spans.forEach((span, index) => {
                if (navLinks?.classList.contains('active')) {
                    if (index === 0) span.style.transform = 'rotate(45deg) translate(10px, 10px)';
                    if (index === 1) span.style.opacity = '0';
                    if (index === 2) span.style.transform = 'rotate(-45deg) translate(7px, -7px)';
                } else {
                    span.style.transform = 'none';
                    span.style.opacity = '1';
                }
            });
        });

        // Cerrar menú al hacer click en un link
        navLinks?.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                navLinks.classList.remove('active');
                mobileToggle.querySelectorAll('span').forEach(span => {
                    span.style.transform = 'none';
                    span.style.opacity = '1';
                });
            });
        });
    }

    // Inicializar otras funcionalidades
    initializeFormValidation();
    initializeFileUpload();
});

// ============== VALIDACIÓN DE FORMULARIOS ==============
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('error');
            input.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            input.classList.remove('error');
            input.style.borderColor = '';
        }

        // Validación de email
        if (input.type === 'email' && input.value.trim()) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
                input.classList.add('error');
                input.style.borderColor = '#dc3545';
                isValid = false;
            }
        }
    });

    return isValid;
}

function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form.id)) {
                e.preventDefault();
                showNotification('Por favor completa todos los campos requeridos', 'warning');
            }
        });
    });
}

// ============== LOGOUT ==============
function logout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        window.location.href = '/logout';
    }
}

// ============== MOSTRAR NOTIFICACIONES ==============
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    const icons = {
        success: 'fas fa-check-circle',
        danger: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };
    
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <i class="${icons[type]}"></i>
        <span>${message}</span>
    `;
    
    // Agregar a un contenedor fijo o al body
    let container = document.querySelector('.notifications-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'notifications-container';
        container.style.position = 'fixed';
        container.style.top = '80px';
        container.style.right = '20px';
        container.style.zIndex = '2000';
        document.body.appendChild(container);
    }
    
    container.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, duration);
}

// ============== CARGAR ARCHIVOS ==============
function initializeFileUpload() {
    const fileUploadGroups = document.querySelectorAll('.file-upload-group');
    
    fileUploadGroups.forEach(group => {
        const input = group.querySelector('input[type="file"]');
        
        if (!input) return;
        
        // Click para seleccionar archivos
        group.addEventListener('click', () => input.click());
        
        // Drag and drop
        group.addEventListener('dragover', (e) => {
            e.preventDefault();
            group.style.borderColor = 'var(--primary-color)';
            group.style.background = 'var(--light-gray)';
        });
        
        group.addEventListener('dragleave', () => {
            group.style.borderColor = 'var(--border-color)';
            group.style.background = '';
        });
        
        group.addEventListener('drop', (e) => {
            e.preventDefault();
            group.style.borderColor = 'var(--border-color)';
            group.style.background = '';
            
            if (e.dataTransfer.files.length > 0) {
                input.files = e.dataTransfer.files;
                handleFileSelection(input);
            }
        });
        
        // Cambio de input
        input.addEventListener('change', () => {
            handleFileSelection(input);
        });
    });
}

function handleFileSelection(input) {
    const previewContainer = document.getElementById('previewContainer');
    
    if (!previewContainer) return;
    
    previewContainer.innerHTML = '';
    
    Array.from(input.files).forEach((file, index) => {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const preview = document.createElement('div');
                preview.className = 'preview-image';
                preview.innerHTML = `
                    <img src="${e.target.result}" alt="Preview">
                    <button type="button" class="preview-remove" onclick="removePreview(${index})">✕</button>
                `;
                previewContainer.appendChild(preview);
            };
            reader.readAsDataURL(file);
        }
    });
}

function removePreview(index) {
    const input = document.getElementById('fotos');
    if (!input) return;
    
    const files = Array.from(input.files);
    files.splice(index, 1);
    
    const dataTransfer = new DataTransfer();
    files.forEach(file => dataTransfer.items.add(file));
    input.files = dataTransfer.files;
    
    handleFileSelection(input);
}

// ============== CAMBIAR ENTRE TABS ==============
function switchTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    const targetTab = document.getElementById(tabName);
    if (targetTab) {
        targetTab.classList.add('active');
        event.target.classList.add('active');
    }
}

// ============== COPIAR AL PORTAPAPELES ==============
function copyToClipboard(text, element) {
    navigator.clipboard.writeText(text).then(() => {
        const originalText = element.textContent;
        element.textContent = '✓ Copiado!';
        setTimeout(() => {
            element.textContent = originalText;
        }, 2000);
    }).catch(() => {
        showNotification('Error al copiar', 'danger');
    });
}

