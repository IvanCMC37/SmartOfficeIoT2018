$(document).ready(function() {
    var year_select = document.getElementById('year');
    var month_select = document.getElementById('month');
    var day_select = document.getElementById('day');
    getPatientAppmts($("#patient").val());
    console.log("$(patient.value---"+$("#patient").val());

    //On Patient change - Populate Appointments
    $("#patient").change(function(){
        console.log("this.value---"+this.value)
        getPatientAppmts(this.value);
        $("#pat_id").val(this.value);
    });

    //On Day change - Populate Appointment Slots
    $("#day").change(function(){
        console.log("$(year.value---"+$("#year").val());
        console.log("$(month.value---"+$("#month").val());
        console.log("this.value---"+this.value)
        console.log("$(doctor.value---"+$("#doctor").val());
        var year=$("#year").val();
        var month=$("#month").val();
        var day=this.value;
        var doctorId=$("#doctor").val();
        getDoctorAvailableSlots(year, month, day, doctorId);
    });

    //Fetch Doctor Availalable Appointment Slots
    function getDoctorAvailableSlots(year, month, day, doctorId){
        $("#slot").children('option:not(:first)').remove();
        alert("called");
        input = {
            "month":month,
            "year":year,
            "day":day,
            "doctor_id":doctorId
        }
        $.ajax({
            type: "POST",
            url: "/api/doctor/daily_check",
            data: JSON.stringify(input),
            success: function(response) {
                console.log((JSON.stringify(response)));
                if(response.days[0]!= null){
                    //Show Available Time Slots 
                    $.ajax({url: "/api/doctorAppmts/"+$("#doctor").val(), success: function(bookedAppmts){
                        var start_time=new Date(response.days[0].start_time);
                        var end_time=new Date(response.days[0].end_time);
                        var timeDifference=(end_time-start_time)/60000;
                        var timeSlots=[];
                        var i=0;
                        while(i<=timeDifference){
                            var timeSlot=new Date(start_time.getTime() + i*60000);
                            var timeSlotLocale=new Date(start_time.getTime() + i*60000).toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
                            timeSlots.push(timeSlotLocale);
                            //Skip if slot is already booked
                            var booked=false;
                            for(var j=0;j<bookedAppmts.length;j++){
                                console.log("bookedAppmts---"+bookedAppmts);
                                console.log("j---"+j);
                                console.log("bookedAppmts[j]---"+bookedAppmts[j]);
                                var bookedSlot=new Date(bookedAppmts[j].start_datetime);
                                console.log("bookedSlot---"+bookedSlot);
                                console.log("timeSlot---"+timeSlot);
                                if(new Date(bookedAppmts[j].start_datetime).getTime() === timeSlot.getTime()){
                                    booked=true;
                                }
                            }
                            //Add if not in Booked Appointments
                            if(booked==false){
                                var str="<option value='" +timeSlot + "'>" +timeSlotLocale + "</option>";
                                $("#slot").append(str);
                            }
                            i+=30;  
                        }
                        console.log("timeSlots---"+timeSlots);
                    }});     
                }
            },
            contentType:"application/json",
            dataType:"json",
        });
    }

    //Fetch Patient Appointments
    function getPatientAppmts(patientId){
        $("#table tbody tr").empty();
        console.log("patientId---"+patientId)
        $.ajax({url: "/api/patientAppmts/"+patientId, success: function(result){
            console.log("patientResultSTRINGIFY---"+JSON.stringify(result));
            console.log("patientResult---"+result);
            var row;
            for(var i=0;i<result.length;i++){
                row="<tr>";
                row=row + "<td>"+ result[i].id +"</td>";
                row=row + "<td>"+ result[i].title +"</td>";
                row=row + "<td>"+ result[i].start_datetime +"</td>";
                row=row + "<td>"+ result[i].end_datetime +"</td>";
                row=row + "<td>"+ result[i].doctor.first_name +" "+result[i].doctor.last_name +"</td>";
                row=row + "<td>"+ "<form action='/patient' method='post'><input type='hidden' name='delete_appmt' value='"+result[i].id+"'><input type='submit' class='btn btn-secondary' value='Delete'/></form></td>";   
                row=row + "</tr>";
                $("#table tbody").append(row);
            }          
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