function hideForm(divId) {
    var form = document.getElementById(divId);

    if(form.style.display === "block") {
        form.style.display = "none";
    } else {
        form.style.display = "block";
    }
}
