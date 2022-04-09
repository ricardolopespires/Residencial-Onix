window.addEventListener("scroll", function(){
	var header = document.querySelector("header");
	header.classList.toggle('sticky', window.scrollY > 0)


})


window.addEventListener("scroll", function(){
	var header = document.querySelector(".navbar");
	header.classList.toggle('secondary', window.scrollY > 0)


})

window.addEventListener("scroll", function(){
	var header = document.querySelector(".ponto");
	header.classList.toggle('ponto_white', window.scrollY > 0)


})