burger=document.querySelector('.burger')
navList=document.querySelector('.navList')
rightNav=document.querySelector('.rightNav')

burger.addEventListener('click', ()=>{
    rightNav.classList.toggle('v-class')
    navList.classList.toggle('v-class')
});
window.onpageshow = function(event) {
    if (event.persisted) {
        window.location.href = "{{ url_for('logout') }}";
    }
};
// JavaScript to add a class on scroll
// const navbar = document.querySelector('.navbar');

// window.addEventListener('scroll', () => {
//     if (window.scrollY > 50) {
//         navbar.classList.add('scrolled');  // Adds class after 50px of scrolling
//     } else {
//         navbar.classList.remove('scrolled');  // Removes class when back to top
//     }
// });
