$(document).ready(function(){
  if (!sessionStorage.getItem("animated")){
    animateNavbar();
    sessionStorage.setItem("animated", "true")
  }
  else {
    $(".fade-in").css("visibility", "visible")
  }
});


let animateNavbar = async () => {
  console.log("animating header")
  const titleFadeSpeed = 1500;
  const itemFadeSpeed = 750;
  const itemDelay = 400

  let title = $(".navbar-brand")
  title.removeClass("fade-in")
  title.css({"opacity": "0"})
  title.animate({"opacity": "1"}, titleFadeSpeed, () => {
    $(".nav-link").removeClass("fade-in")
    $(".nav-link").css({"opacity": "0"})
    $(".nav-link").each(function(i, elem){
      let item = $(elem)
      item.delay(i * itemDelay).animate({"opacity": "1"}, itemFadeSpeed)
    })
  })

}