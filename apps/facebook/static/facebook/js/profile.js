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