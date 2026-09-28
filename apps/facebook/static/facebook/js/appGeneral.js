// const toastTrigger = document.getElementById('liveToastBtn')
// const toastLiveExample = document.getElementById('liveToast')

// if (toastTrigger) {
//     const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
//     toastTrigger.addEventListener('click', () => {
//     toastBootstrap.show()
//     })
// }

// Toasts
const toastEls = document.querySelectorAll('.toast')

toastEls.forEach(toastEl => {
    const toast = new bootstrap.Toast(toastEl)
    toast.show()
})

// Forms
document.querySelectorAll('input, textarea').forEach(element => {
    element.addEventListener('input', function () {
        this.classList.remove('is-invalid');
    });
});