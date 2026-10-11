// Editar foto de perfil
const photoButton = document.getElementById("profile-button-photo");
const photoInput = document.getElementById("id_photo");
const photoPreview = document.getElementById("profile-preview-photo");

photoButton.addEventListener("click", () => {
	photoInput.click();
});

photoInput.addEventListener("change", () => {
	const file = photoInput.files[0];

	if (!file) return;

	const imageUrl = URL.createObjectURL(file);

	if (photoPreview.tagName === "IMG") {
		photoPreview.src = imageUrl;
	} else {
		photoPreview.replaceChildren();
		photoPreview.style.backgroundImage = `url("${imageUrl}")`;
		photoPreview.style.backgroundSize = "cover";
		photoPreview.style.backgroundPosition = "center";
		photoPreview.style.backgroundRepeat = "no-repeat";
	}
});
