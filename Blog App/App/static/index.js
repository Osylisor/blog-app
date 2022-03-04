closeButton = document.querySelector('.close-button');

closeButton.addEventListener('onclick', closeBtn())


closeBtn = () =>{
    this.parentElement.style.display = "none";
}