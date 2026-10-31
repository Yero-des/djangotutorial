// Vista previa interactiva de la imagen de la publicación
(() => {
	"use strict";

	const imageInput = document.getElementById("id_image");
	const picker = document.getElementById("post-image-picker");
	const preview = document.getElementById("post-image-preview");
	const placeholder = document.getElementById("post-image-placeholder");
	const errorsList = document.getElementById("post-image-errors");
	const fieldLabel = document.querySelector('label[for="id_image"]');

	if (!imageInput || !picker || !preview || !placeholder || !errorsList) {
		return;
	}

	const maxSize = Number(imageInput.dataset.maxSize) || 5 * 1024 * 1024;
	let previewUrl = null;

	const showErrors = (messages) => {
		errorsList.replaceChildren(
			...messages.map((message) => {
				const item = document.createElement("li");
				item.textContent = message;
				return item;
			}),
		);
		errorsList.classList.remove("d-none");
		errorsList.classList.add("d-block");
		picker.classList.add("border-danger");
	};

	const clearErrors = () => {
		errorsList.replaceChildren();
		errorsList.classList.remove("d-block");
		errorsList.classList.add("d-none");
		picker.classList.remove("border-danger");
	};

	const setPreview = (file) => {
		if (previewUrl) {
			URL.revokeObjectURL(previewUrl);
		}

		previewUrl = URL.createObjectURL(file);
		preview.src = previewUrl;
		preview.classList.remove("d-none");
		placeholder.classList.add("d-none");
		picker.classList.add("has-image");
	};

	const resetPreview = () => {
		if (previewUrl) {
			URL.revokeObjectURL(previewUrl);
			previewUrl = null;
		}

		preview.removeAttribute("src");
		preview.classList.add("d-none");
		placeholder.classList.remove("d-none");
		picker.classList.remove("has-image");
	};

	const validateFile = (file) => {
		if (!file.type.startsWith("image/")) {
			return "El archivo debe ser una imagen JPG, PNG o WebP.";
		}

		if (file.size > maxSize) {
			const maxMb = Math.round(maxSize / (1024 * 1024));
			return `La imagen no puede superar los ${maxMb} MB.`;
		}

		return null;
	};

	const handleFile = (file) => {
		clearErrors();

		if (!file) {
			resetPreview();
			return;
		}

		const error = validateFile(file);

		if (error) {
			imageInput.value = "";
			resetPreview();
			showErrors([error]);
			return;
		}

		setPreview(file);
	};

	const openFileDialog = () => imageInput.click();

	picker.addEventListener("click", openFileDialog);

	fieldLabel?.addEventListener("click", (event) => {
		event.preventDefault();
		openFileDialog();
	});

	imageInput.addEventListener("change", () => {
		handleFile(imageInput.files[0]);
	});

	// Arrastrar y soltar una imagen sobre la vista previa
	picker.addEventListener("dragenter", (event) => {
		event.preventDefault();
		picker.classList.add("is-dragging");
	});

	picker.addEventListener("dragover", (event) => {
		event.preventDefault();
	});

	picker.addEventListener("dragleave", (event) => {
		if (!picker.contains(event.relatedTarget)) {
			picker.classList.remove("is-dragging");
		}
	});

	picker.addEventListener("drop", (event) => {
		event.preventDefault();
		picker.classList.remove("is-dragging");

		const file = event.dataTransfer?.files?.[0];

		if (!file) {
			return;
		}

		try {
			const transfer = new DataTransfer();
			transfer.items.add(file);
			imageInput.files = transfer.files;
		} catch {
			showErrors([
				"Tu navegador no permite arrastrar la imagen. Usa el selector.",
			]);
			return;
		}

		handleFile(file);
	});
})();
