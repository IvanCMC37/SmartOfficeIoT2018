$(document).ready(function() {
    var year_select = document.getElementById('year');
    var month_select = document.getElementById('month');
    var day_select = document.getElementById('day');

    //Fetch Appointments
    getAllAppmts();
    if(window.location.href.includes("patient")){
        getPatientAppmts($("#patient").val());
    }
    else getDoctorAppmts($("#doctor").val());
    $("#pat_id").val($("#patient").val());
    $("#doctor_id").val($("#doctor").val());

    //On Patient change - Populate Appointments
    $("#patient").change(function(){
        getPatientAppmts(this.value);
        $("#pat_id").val(this.value);
    });

    //On Doctor change - Populate Appointments
    $("#doctor").change(function(){
        getDoctorAppmts(this.value);
        $("#doctor_id").val(this.value);
    });

    //On Day change - Populate Appointment Slots
    $("#day").change(function(){
        var year=$("#year").val();
        var month=$("#month").val();
        var day=this.value;
        var doctorId=$("#doctor").val();
        getDoctorAvailableSlots(year, month, day, doctorId);
    });

    //Fetch Doctor Availalable Appointment Slots
    function getDoctorAvailableSlots(year, month, day, doctorId){
        $("#slot").children('option:not(:first)').remove();
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
                                var bookedSlot=new Date(bookedAppmts[j].start_datetime);
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
            var appointments=JSON.stringify(result);
            appointments=appointments.replace("start_datetime", "start");
            appointments=appointments.replace("end_datetime", "end");
            appointments= JSON.parse(appointments);
            $('#calendar').fullCalendar( 'removeEvents')
            $('#calendar').fullCalendar( 'addEventSource', appointments )    
        }});
    }

    //Fetch Doctor Appointments
    function getDoctorAppmts(doctorId){
        $("#table tbody tr").empty();
        $.ajax({url: "/api/doctorAppmts/"+doctorId, success: function(result){
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
            var appointments=JSON.stringify(result);
            appointments=appointments.split("start_datetime").join("start");
            appointments=appointments.split("end_datetime").join("end");
            appointments= JSON.parse(appointments);
            $('#calendar').fullCalendar( 'removeEvents')
            $('#calendar').fullCalendar( 'addEventSource', appointments )    
        }});
    }

    //Fetch Doctor Availalable Appointment Slots
    function getDoctorAvailableSlots(year, month, day, doctorId){
        $("#slot").children('option:not(:first)').remove();
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
                                var bookedSlot=new Date(bookedAppmts[j].start_datetime);
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
                    }});     
                }
            },
            contentType:"application/json",
            dataType:"json",
        });
    }

    //Fetch All Appointments
    function getAllAppmts(){
        $.ajax({url: "/api/appointment", success: function(result){
            var doctor_appmtCount={};
            for(var i=0;i<result.length;i++){
                var doctor=result[i].doctor.first_name +" "+result[i].doctor.last_name;
                if(doctor_appmtCount[doctor]!=undefined){
                    doctor_appmtCount[doctor]=doctor_appmtCount[doctor]+1;
                }
                else doctor_appmtCount[doctor]=1;
            }
            var new_result=[];
            var result = Object.keys(doctor_appmtCount).map(function(key) {
                new_result.push([key, doctor_appmtCount[key]]);
            });
            // Load the Visualization API and the corechart package.
            google.charts.load('current', {'packages':['corechart']});

            // Set a callback to run when the Google Visualization API is loaded.
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {

                // Create the data table.
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Topping');
                data.addColumn('number', 'Slices');
                data.addRows(new_result);

                // Set chart options
                var options = {'title':'Doctors with Total Appointments',
                            'width':600,
                            'height':400};

                // Instantiate and draw our chart, passing in some options.
                var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
                chart.draw(data, options);
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
        getDoctorAvailableSlots(year, month, 1, $("#doctor_id").val());
        day_select.innerHTML=optionHTML;
    }
    //Populating Full Calendar UI with Appointments
    var d = new Date();
    var month = d.getMonth()+1;
    var day = d.getDate();
    var today = d.getFullYear() + '-' +
        ((''+month).length<2 ? '0' : '') + month + '-' +
        ((''+day).length<2 ? '0' : '') + day;
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
            $('#calendar').fullCalendar('renderEvent', eventData, false); // stick? = true
        }
        $('#calendar').fullCalendar('unselect');
        },
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        events: []
    })
});