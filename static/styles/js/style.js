// Form animation
$("#modalBtn").click(function(e){
    $(".modal").fadeIn(500);
    e.stopImmediatePropagation(); // Stops other handlers from executing
});

 $("#closeBtn").click(function(){
    $(".modal").fadeOut(500);
});

$(document).click(function(e) {
    if (!$(e.target).closest('#patient-modal').length) {
        $('.modal').fadeOut();
    }
});