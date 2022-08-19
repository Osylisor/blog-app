const menuBar = document.querySelector('.menu');
const navList = document.querySelector('.nav-list');


menuBar.addEventListener('click', ()=>{

    navList.classList.toggle('active');
});