/**
 * DESCRIPTION: this file contains the code to show the post image in a popup and in a carousel
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

document.addEventListener("DOMContentLoaded", () => {
  const wrapper = document.querySelector(".carousel-wrapper");
  const slides = document.querySelectorAll(".carousel-slide");
  const prevBtn = document.getElementById("carousel-btn");
  const nextBtn = document.getElementById("carousel-btn");

  if (!wrapper || !slides) {
    return;
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