// Forms
document.querySelectorAll("input, textarea").forEach((element) => {
	element.addEventListener("input", function () {
		this.classList.remove("is-invalid");
	});
});

// Like inner post
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
