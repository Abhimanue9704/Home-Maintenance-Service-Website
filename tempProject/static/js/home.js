// const observer = new IntersectionObserver((entries) => {
//     entries.forEach((entry) =>{
//         if(entry.isIntersecting){
//             entry.target.classList.add('show');
//         }
//         else{
//             entry.target.classList.remove('show');
//         }
//     });
// });

// const hiddenelements = document.querySelector('.hidden');
// hiddenelements.forEach((el) => observer.observe(el));

const observer = new IntersectionObserver((entries) => {
    Array.from(entries).forEach((entry) => {
        if(entry.isIntersecting){
            entry.target.classList.add('show');
        }
        else{
            entry.target.classList.remove('show');
        }
    });
});

const hiddenelements = document.querySelectorAll('.hidden');
Array.from(hiddenelements).forEach((el) => observer.observe(el));

var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-60px";
  }
  prevScrollpos = currentScrollPos;
}

let slideIndex = 0;
showSlides();

function showSlides() {
  let i;
  let slides = document.getElementsByClassName("slides");
  let dots = document.getElementsByClassName("dot");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}    
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
  setTimeout(showSlides, 10000); // Change image every 2 seconds
}
const observe = new IntersectionObserver((entries) => {
  Array.from(entries).forEach((entry) => {
      if(entry.isIntersecting){
          entry.target.classList.add('trans-end');
      }
      else{
          entry.target.classList.remove('trans-end');
      }
  });
});

const hiddenelement = document.querySelectorAll('.trans-on');
Array.from(hiddenelement).forEach((el) => observe.observe(el));