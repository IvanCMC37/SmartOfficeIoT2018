//Get modal elements

var modal = document.getElementById('modal');

// Get open modal button
var modalBtn = document.getElementById('modalBtn');

//Get close button
var closeBtn = document.getElementsByClassName('closeBtn')[0];

//Listen for clicks
modalBtn.addEventListener('click', openAppointmentForm);
closeBtn.addEventListener('click', closeAppointmentForm);
//Listen for outside click
window.addEventListener('click', outsideClick);


//Function to open modal
function openAppointmentForm(){
    modal.style.display = 'block';
}

function closeAppointmentForm(){
    modal.style.display = 'none';
}

function outsideClick(e){
    if(e.target == modal){

        modal.style.display = 'none';
    }
}

