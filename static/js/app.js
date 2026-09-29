// Toasts
const toastEls = document.querySelectorAll('.toast')

toastEls.forEach(toastEl => {
    const toast = new bootstrap.Toast(toastEl)
    toast.show()
})