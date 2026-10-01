// Editar foto de perfil
const photoButton = document.getElementById('profile-button-photo');
const photoInput = document.getElementById('id_photo');
const photoPreview = document.getElementById('profile-preview-photo');

photoButton.addEventListener('click', () => {
    photoInput.click();
});

photoInput.addEventListener('change', () => {
    const file = photoInput.files[0];

    if (!file) return;

    photoPreview.src = URL.createObjectURL(file);
});

// Modo estado de modo oscuro
const darkModeToggle = document.getElementById('dark-mode-toggle')
const darkModeLabel = document.getElementById('dark-mode-label')
const url = darkModeToggle.dataset.url
const csrfToken = darkModeToggle.dataset.csrf

darkModeToggle.addEventListener('change', function () {

    document.documentElement.setAttribute(
        'data-bs-theme',
        this.checked ? 'dark' : 'light'
    );

    const darkModeIcon = darkModeLabel.firstElementChild

    darkModeIcon.classList.remove('bi-moon-stars', 'bi-moon-stars-fill')
    const toggleClass = `bi-moon-stars${ this.checked ? '-fill' : ''}`
    darkModeIcon.classList.add(toggleClass)

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }

    }).then(response => {
        if (!response.ok) {
            alert('Ha ocurrido un error temporal')
        }
    })
})