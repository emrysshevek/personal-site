$(document).ready(function(){
    $(".project").each(function(i, elem){
      let bound = elem.getBoundingClientRect()
      let img = $(elem).find(".project-img")
      let p = $(elem).find(".project-text")
      img.css("top", -bound.top)
    })


    $(".project").each(function(i, elem) {
        $(elem).on("mouseenter", function() {
            $(elem).css("background-size", "105% auto")
            $(elem).css("background-position", "top -20px left -20px")
        }).on("mouseleave", function() {
            $(elem).css("background-size", "100% auto")
            
            $(elem).css("background-position", "top 0px left 0px")
        })
        
    })
});

$(document).on("scroll", function() {
    $(".project").each(function(i, elem){
      let bound = elem.getBoundingClientRect()
      let img = $(elem).find(".project-img")
      let p = $(elem).find(".project-text")
      img.css("top", -bound.top)
    })
})


