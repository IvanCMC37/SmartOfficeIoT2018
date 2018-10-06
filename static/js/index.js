$(document).ready(function() {
    var year_select = document.getElementById('year');
    var month_select = document.getElementById('month');
    var day_select = document.getElementById('day');
    getPatientAppmts($("#patient").val());
    console.log("$(patient.value---"+$("#patient").val())

    //On Patient change - Populate Appointments
    $("#patient").change(function(){
        console.log("this.value---"+this.value)
        getPatientAppmts(this.value);
    });

    //Fetch Patient Appointments
    function getPatientAppmts(patientId){
        $("#table tbody tr").empty();
        console.log("patientId---"+patientId)
        $.ajax({url: "/api/patientAppmts/"+patientId, success: function(result){
            console.log("patientResultSTRINGIFY---"+JSON.stringify(result));
            console.log("patientResult---"+result);
            patientResult=result[0];
            var row="<tr>";
                row=row + "<td>"+ patientResult.id +"</td>";
                row=row + "<td>"+ patientResult.title +"</td>";
                row=row + "<td>"+ patientResult.start_datetime +"</td>";
                row=row + "<td>"+ patientResult.end_datetime +"</td>";
                row=row + "<td>"+ patientResult.doctor.first_name +" "+patientResult.doctor.last_name +"</td>";
                row=row + "</tr>";
            $("#table tbody").append(row);
        }});
    }

    //On Month select - Populate Days 
    month_select.onchange =function(){
        month = month_select.value;
        year = year_select.value;
        day = 0;
        optionHTML ='';
        if (month==2){
            if((year%4==0 && year%100!=0 )||(year%400==0)){
                day =29;
            }
            else{
                day =28;
            }
        }
        else if (month==1 ||month==3||month==5||month==7||month==8||month==10||month==12){
            day =31;
        }
        else{
            day=30;
        }
        for(i =1; i<=day; i++){
            optionHTML +='<option value="'+i+'">'+i+'</option>';
        }
        day_select.innerHTML=optionHTML;
    }
    //Populating Full Calendar UI with Appointments
    var d = new Date();
    var month = d.getMonth()+1;
    var day = d.getDate();
    var today = d.getFullYear() + '-' +
        ((''+month).length<2 ? '0' : '') + month + '-' +
        ((''+day).length<2 ? '0' : '') + day;
        console.log("appointments---"+appointments);
        appointments=appointments.replace("start_datetime", "start");
        appointments=appointments.replace("end_datetime", "end");
        appointments= JSON.parse(appointments);
        console.log(appointments[0].start);
        console.log("appointments---"+appointments);
    $('#calendar').fullCalendar({
        defaultDate: today,
        defaultView: 'agendaWeek',
        weekends: false,
        navLinks: true, // can click day/week names to navigate views
        selectable: true,
        selectHelper: true,
        select: function(start, end) {
        var title = prompt('Book Appointment:');
        var eventData;
        if (title) {
            eventData = {
            title: title,
            start: start,
            end: end
            };
            $('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true
        }
        $('#calendar').fullCalendar('unselect');
        },
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        events: appointments
    })

});