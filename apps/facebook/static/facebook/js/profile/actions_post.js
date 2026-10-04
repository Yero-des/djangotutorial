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
