document.addEventListener('DOMContentLoaded', function () {
    const textElement = document.getElementById('text');
    const text = textElement.innerText; // Get the text content
    textElement.innerHTML = ''; // Clear the existing text

    // Wrap each letter in a span with an animation delay
    text.split('').forEach((letter, index) => {
        const span = document.createElement('span');
        span.innerText = letter;
        span.style.setProperty('--i', index); // Set custom property for animation delay
        textElement.appendChild(span);
    });
});