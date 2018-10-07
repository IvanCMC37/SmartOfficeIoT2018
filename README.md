# Smart Office Internet Of Things (IoT) Semester 2 2018

> __Contributors:__ David B, Ivan C, Jitender P

> David's branch is 'patient'<br>
> Ivan's branch is 'doctor'<br>
> Jitender's branch is 'clerk'<br>

The web app does not use a login system and UI features have been included to allow for the changing of users.

`/patient`
* A patient can view his appointments, create new appointments, register themselves as a patient and delete appointments.
* As a user, I can switch patients with the use of a combobox and display that patient’s appointments
* When an appointment is submitted, two requests are made. One is an ajax request that hits the patient_api endpoint and then makes a post request to the cloud database.  The other hits the google calendar api and posts the appointment into the doctors google calendar.

`/doctor`
* A doctor is able to pull up patients data as well as view his weekly schedule and make notes and diagnoses.  When notes and a diagnoses are made, the ( patient history ) endpoint is hit and added to the database.
* A doctor can also provide his availability on a weekly basis which talks to the google calendar.

`/clerk`
* A medical clerk is able to add and delete appointments from a calendar based on the doctor’s schedule. The clerk is able to handle schedules for all of the doctors.

Validation controls have been implemented across all the pages.

`gRPC`

* When a patient arrives at the doctor’s office, he is able to let the doctor know he has arrived with the help of Google Assistant and a command “My name is ...” .  This works with the use of gRPC and allows the front office pi to communicate with the doctor’s pi and notify him/her.


Database Schema
============

![alt text](https://i.imgur.com/N4DOdeI.png)

Documentation
===========

Sphinx and Pydocs was used for documentation and can be accessed and ran on a separate server `./sphinx-server.sh`
