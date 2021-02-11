// Change log in modal title to reuse the same log in modal with different heads!
function logInmodalTitle(text) {
    $('.log-in-title').text(text);
}

// Scroll with mouse
const slider = document.querySelector('.related-page-div')
let isDown = false;
let startX;
let scrollLeft;

slider.addEventListener('mousedown', (e) => {
    e.preventDefault();
    isDown = true;
    startX = e.pageX - slider.offsetLeft;
    scrollLeft = slider.scrollLeft;
});

slider.addEventListener('mouseleave', (e) => {
    e.preventDefault();
    isDown = false;
});

slider.addEventListener('mouseup', (e) => {
    e.preventDefault();
    isDown = false;
});

slider.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - slider.offsetLeft;
    const walk = (x - startX) * 1.3;
    slider.scrollLeft = scrollLeft - walk;
});