const images = [
  "../static/assets/img/1.jpg",
  "../static/assets/img/2.jpg",
  "../static/assets/img/3.jpg",
  "../static/assets/img/4.jpg",
  "../static/assets/img/5.jpg",
  "../static/assets/img/6.jpg",
  "../static/assets/img/7.jpg",
];
const number = Math.floor(Math.random() * images.length);
const bgImage = "url('" + images[number] + "')";

document.body.style.backgroundImage = bgImage;
document.body.style.backgroundSize = "100%";
document.body.style.backgroundRepeat = "no-repeat";
