let slide = 0;
var add = i => i+1;
var subtract = i => i-1;

function changeSlide(direction) {
    let SLIDE_NUM = document.querySelectorAll('.slide-number');
    window.app.SLIDES[slide].style.display='none';
    slide = direction(slide)
    if (slide==window.app.SLIDES.length) {
        slide = 0
    }
    if (slide==-1) {
        slide = window.app.SLIDES.length-1
    }
    window.app.SLIDES[slide].style.display='flex';
    SLIDE_NUM[slide].innerHTML = `${slide+1} <i>of</i> ${window.app.SLIDES.length}`;
}

function slideNavShow(elem) {
    elem.style.opacity=100;
}

function slideNavHide(elem) {
    elem.style.opacity=0;
}


document.addEventListener("DOMContentLoaded", function () {
    if (document.querySelector('.post-slideshow')) {
        const NEXT = document.querySelector('#next-slide');
        const PREV = document.querySelector('#prev-slide');
        var SLIDES = document.querySelectorAll('.slideshow-container');
        let SLIDE_NUM = document.querySelectorAll('.slide-number');
        SLIDES[0].style.display="flex";

        if (SLIDES.length > 1) {
            SLIDE_NUM[0].innerHTML = `1 <i>of</i> ${SLIDES.length}`;
            window.app.SLIDES = SLIDES;
            NEXT.style.cursor = "pointer";
            PREV.style.cursor = "pointer";

            NEXT.addEventListener('mouseenter', function(e) {return slideNavShow(e.target)} )
            NEXT.addEventListener('mouseleave', function(e) {return slideNavHide(e.target)} )

            PREV.addEventListener('mouseenter', function(e) {return slideNavShow(e.target)} )
            PREV.addEventListener('mouseleave', function(e) {return slideNavHide(e.target)} )

            NEXT.addEventListener('click', function() { return changeSlide(add)})
            PREV.addEventListener('click', function() { return changeSlide(subtract)}) 
        }

    }
})

