// Formularios
document.querySelectorAll("input, textarea").forEach((element) => {
	element.addEventListener("input", function () {
		this.classList.remove("is-invalid");
	});
});

document.querySelectorAll(".new-comment-form").forEach((form) => {
	const imageInput = form.querySelector("[data-comment-image-input]");
	const preview = form.querySelector("[data-comment-image-preview]");
	const previewImage = form.querySelector("[data-comment-image-preview-img]");
	let previewUrl;

	imageInput.addEventListener("change", () => {
		const image = imageInput.files[0];

		if (!image) return;

		if (previewUrl) URL.revokeObjectURL(previewUrl);
		previewUrl = URL.createObjectURL(image);
		previewImage.src = previewUrl;
		preview.hidden = false;
	});

	form.querySelector("[data-comment-image-remove]").addEventListener(
		"click",
		() => {
			imageInput.value = "";
			previewImage.removeAttribute("src");
			preview.hidden = true;
			if (previewUrl) URL.revokeObjectURL(previewUrl);
			previewUrl = null;
		},
	);
});

// Like dentro del post
async function likePost(element) {
	const postId = element.dataset.postId;
	const buttons = [...document.querySelectorAll(".btn-like-inner-post")].filter(
		(button) => button.dataset.postId === postId,
	);

	buttons.forEach((button) => {
		button.disabled = true;
	});

	try {
		const response = await fetch(element.dataset.url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": element.dataset.csrf,
			},
		});
		const data = await response.json();

		if (!response.ok || data.status !== "ok") {
			throw new Error("No se pudo actualizar el me gusta.");
		}

		const likesSpan = element.querySelector("small");
		const numberLikes =
			Number(likesSpan.textContent) + (data.liked ? 1 : -1);

		buttons.forEach((button) => {
			button.classList.toggle("liked", data.liked);
			button.querySelector("small").textContent = numberLikes;
		});
	} catch {
		alert("Ha ocurrido un error temporal");
	} finally {
		buttons.forEach((button) => {
			button.disabled = false;
		});
	}
}

// Seguir o dejar de seguir al autor de una publicación
document.addEventListener("click", async (event) => {
	const link = event.target.closest(".js-follow-toggle");

	if (!link) return;

	event.preventDefault();
	event.stopPropagation();

	try {
		const response = await fetch(link.dataset.url, {
			method: "POST",
			headers: {
				"X-CSRFToken": link.dataset.csrf,
				"X-Requested-With": "XMLHttpRequest",
			},
		});
		const data = await response.json();

		if (!response.ok || data.status !== "ok") {
			throw new Error("No se pudo actualizar el seguimiento.");
		}

		link.classList.toggle("text-danger", data.is_following);
		link.classList.toggle("text-primary", !data.is_following);
		link.textContent = data.is_following ? "Dejar de seguir" : "Seguir";
	} catch {
		alert("Ha ocurrido un error temporal");
	}
});

// Cambiar tema
const darkModeToggle = document.getElementById("dark-mode-toggle");
const darkModeLabel = document.getElementById("dark-mode-label");
const url = darkModeToggle.dataset.url;
const csrfToken = darkModeToggle.dataset.csrf;

darkModeToggle.addEventListener("change", function () {
	document.documentElement.setAttribute(
		"data-bs-theme",
		this.checked ? "dark" : "light",
	);

	const darkModeIcon = darkModeLabel.firstElementChild;

	darkModeIcon.classList.remove("bi-moon-stars", "bi-moon-stars-fill");
	const toggleClass = `bi-moon-stars${this.checked ? "-fill" : ""}`;
	darkModeIcon.classList.add(toggleClass);

	fetch(url, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrfToken,
		},
	}).then((response) => {
		if (!response.ok) {
			alert("Ha ocurrido un error temporal");
		}
	});
});

// Acciones dentro de publicación
function swalTheme() {
	return document.documentElement.dataset.bsTheme === "dark"
		? "dark"
		: "light";
}

document.addEventListener("submit", (event) => {
	const form = event.target;

	if (form.matches(".new-comment-form")) {
		event.preventDefault();
		submitComment(form);
		return;
	}

	if (!form.matches(".delete-post-form")) {
		return;
	}

	event.preventDefault();

	Swal.fire({
		title: "¿Eliminar publicación?",
		text: "Esta acción no se puede deshacer.",
		icon: "warning",
		showCancelButton: true,
		confirmButtonText: "Sí, eliminar",
		cancelButtonText: "Cancelar",
		buttonsStyling: false,
		theme: swalTheme(),
		customClass: {
			popup: "border-0 shadow rounded-3",
			title: "text-body",
			htmlContainer: "text-body-secondary",
			confirmButton: "btn btn-danger",
			cancelButton: "btn btn-secondary ms-2",
		},
	}).then((result) => {
		if (result.isConfirmed) {
			HTMLFormElement.prototype.submit.call(form);
		}
	});
});

// Subir comentario
async function submitComment(form) {
	const submitButton = form.querySelector('button[type="submit"]');
	const textArea = form.querySelector('textarea[name="comment"]');
	const commentsSection = form
		.closest(".modal")
		.querySelector("[data-comments-list]");

	submitButton.disabled = true;

	try {
		const response = await fetch(form.action, {
			method: "POST",
			headers: {
				"X-CSRFToken": form.querySelector(
					'[name="csrfmiddlewaretoken"]',
				).value,
			},
			body: new FormData(form),
		});
		const data = await response.json();

		if (!response.ok) {
			throw data;
		}

		commentsSection.querySelector("[data-empty-comments]")?.remove();

		const commentWrapper = document.createElement("div");
		if (data.comments_count % 2 === 0) {
			commentWrapper.className =
				"bg-body-tertiary border-bottom border-top";
		}
		commentWrapper.innerHTML = data.comment_html;
		commentsSection.prepend(
			commentWrapper.firstElementChild || commentWrapper,
		);

		form.querySelector("textarea").value = "";
		form.querySelector("[data-comment-image-remove]").click();
		form
			.closest(".modal")
			.querySelector("[data-comments-count]").textContent =
			data.comments_count;

		// Mostrar toast de comentario agregado
		toastFetch(data.success_html);
	} catch (error) {
		// Marcar textarea con un tono rojo
		textArea.classList.add("is-invalid");

		// Mostrar toast de error
		toastFetch(error.error_html);
	} finally {
		submitButton.disabled = false;
	}
}
