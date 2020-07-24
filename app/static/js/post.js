

function changeSlide(direction) {
   console.log(direction)

}

//init()

document.addEventListener("DOMContentLoaded", function () {
    if (document.querySelector('.post-slideshow')) {
        console.log('slideshow')
        const next = document.querySelector('#next-slide');
        const prev = document.querySelector('#prev-slide');

        const SLIDES = document.querySelectorAll('.slideshow-container');
        console.log(SLIDES)
        SLIDES[0].style.display="flex";

        next.addEventListener('click', function () { return changeSlide('next')})
        prev.addEventListener('click', function() { return changeSlide('prev')})
    }
})

