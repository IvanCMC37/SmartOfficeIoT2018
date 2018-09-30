$(document).ready(function() {
    
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
        //console.log(appointments[0].start);
        console.log("appointments---"+appointments);
    $('#calendar').fullCalendar({
        defaultDate: today,
        defaultView: 'agendaWeek',
        minTime: "09:00:00",
        maxTime: "17:30:00",
        height: "auto",
        allDaySlot: false,
        weekends: false,
        navLinks: true, // can click day/week names to navigate views
        selectable: false,
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