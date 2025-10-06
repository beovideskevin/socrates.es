/**
 * Usage:

    <p>
        <span id="random1" class="random-wrapper">
            <span>Line 1</span>
            <span>Line 2</span>
            <span>Line 3</span>
        </span>
    </p>
 */
document.addEventListener("DOMContentLoaded", () => {
    shuffle();
    const timerId = setInterval(shuffle, 300000);
});

function shuffle() {
    $(".random-wrapper").each((index, wrapper) => {
       shuffleElement($(wrapper)); 
       wrapper.animate([{
            backgroundColor: "#e8e8e8"
       },{
            backgroundColor: "white"
        }], 3000);
    });
}

function shuffleElement(wrapper) {
    const children = wrapper.children();
    // Convert jQuery object to a plain array
    const elementsArray = children.get();
    // Shuffle the array of elements
    const shuffledElements = shuffleArray(elementsArray);
    // Re-append the shuffled elements to the container
    wrapper.empty(); // Clear existing children
    for (const element of shuffledElements) {
        wrapper.append(element);
    }
}

// Function to shuffle an array (Fisher-Yates shuffle)
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]]; // Swap elements
  }
  return array;
}