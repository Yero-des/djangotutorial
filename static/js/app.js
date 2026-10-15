// Toasts
const toastContainer = document.getElementById("toastContainer");
const toastEls = document.querySelectorAll(".toast");

toastEls.forEach((toastEl) => {
	const toast = new bootstrap.Toast(toastEl);
	toast.show();
});

// Toast en peticiones fetch (sin recargar)
function toastFetch(errorHtml) {
	// Enviar un toast de error con los datos json
	const errorWraper = document.createElement("div");
	errorWraper.innerHTML = errorHtml;
	const toastBootstrap = bootstrap.Toast.getOrCreateInstance(
		errorWraper.firstElementChild,
	);

	// Agregar errorWraper al DOM
	toastContainer.prepend(errorWraper.firstElementChild || errorWraper);
	toastBootstrap.show();
}
