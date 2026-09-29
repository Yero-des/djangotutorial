// Forms
document.querySelectorAll('input, textarea').forEach(element => {
    element.addEventListener('input', function () {
        this.classList.remove('is-invalid');
    });
});