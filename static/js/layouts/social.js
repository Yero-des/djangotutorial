// Formularios
document.querySelectorAll("input, textarea").forEach((element) => {
	element.addEventListener("input", function () {
		this.classList.remove("is-invalid");
	});
});

// Like dentro del post
function likePost(element) {
	const likesSpan = element.getElementsByTagName("span")[0];
	const url = element.dataset.url;
	const csrfToken = element.dataset.csrf;

	let numberLikes = Number(likesSpan.innerHTML);

	fetch(url, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrfToken,
		},
	})
		.then((response) => {
			if (!response) {
				alert("Ha ocurrido un error temporal");
			}
			return response.json();
		})
		.then((data) => {
			if (data.status == "ok") {
				if (data.liked) {
					numberLikes++;
					element.classList.add("liked");
				} else {
					numberLikes--;
					element.classList.remove("liked");
				}
				likesSpan.innerHTML = numberLikes;
			}
		});
}

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
