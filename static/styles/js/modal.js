
// Register a patient

$("#registerModal").click(function(e){
    $(".modal2").fadeIn(500);
    e.stopImmediatePropagation(); // Stops other handlers from executing
});

$("#closeBtnReg").click(function(){
    $(".modal2").fadeOut(500);
});

$(document).click(function(e) {
    if (!$(e.target).closest('#register-modal').length) {
        $('.modal2').fadeOut();
    }
});

// Book Appointment Form animation
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


// https://jqueryui.com/datepicker
$(function() {
    $("#datepicker").datepicker();
  } );
