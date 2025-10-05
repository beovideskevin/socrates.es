/**
 * Usage:

  <img class="postImg" src="/static/assets/images/blog/david-dead-of-socrates.jpg" alt="La muerte de Sócrates, por Jacques-Louis David (1787)">
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


/**
 * Usage:

    <div class="carousel-container">
      <div class="carousel-wrapper">
        <div class="carousel-slide">
            <img src="/static/assets/images/art/athens-show-02.jpg" alt="Yo frente a mi obra el día de la inauguración." class="postImg">
        </div>
        <div class="carousel-slide">
            <img src="/static/assets/images/social.jpg" alt="Todos los hombres son mortales, Sócrates es un hombre, Sócrates es mortal." class="postImg">
        </div>
        <div class="carousel-slide">
            <img src="/static/assets/images/art/athens-show-03.jpg" alt="La posición de la galería en el mapa." class="postImg">
        </div>
      </div>
      <button id="carousel-prev-btn" class="fa fa-arrow-left"></button>
      <button id="carousel-next-btn" class="fa fa-arrow-right"></button>
    </div>

 */
document.addEventListener("DOMContentLoaded", () => {
  const wrapper = document.querySelector(".carousel-wrapper");
  const slides = document.querySelectorAll(".carousel-slide");
  const prevBtn = document.getElementById("carousel-prev-btn");
  const nextBtn = document.getElementById("carousel-next-btn");

  if (!wrapper || !slides || !prevBtn || !nextBtn) {
    return false;
  }

  let currentSlide = 0;

  // Function to move to a specific slide
  function goToSlide(index) {
    if (index < 0) {
      currentSlide = slides.length - 1; // Loop back to the last slide
    } else if (index >= slides.length) {
      currentSlide = 0; // Loop back to the first slide
    } else {
      currentSlide = index;
    }
    const offset = -currentSlide * 100;
    wrapper.style.transform = `translateX(${offset}%)`;
  }

  // Event listener for the "Next" button
  nextBtn.addEventListener("click", () => {
    goToSlide(currentSlide + 1);
  });

  // Event listener for the "Previous" button
  prevBtn.addEventListener("click", () => {
    goToSlide(currentSlide - 1);
  });
});