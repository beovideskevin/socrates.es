/**
 * DESCRIPTION: this file contains the code to show the post image in a popup
 */
$(document).ready(function() {
    const modal = document.getElementById("modal");
    const modalImg = document.getElementById("imgModal");
    const captionText = document.getElementById("caption");

    $(".postImg").on('click', function() {
        modal.style.display = "block";
        modalImg.src = this.src;
        captionText.innerHTML = this.alt;
    });

    modal.onclick = function() {
        modal.style.display = "none";
    }
});