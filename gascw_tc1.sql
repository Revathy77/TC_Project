create database gascw_tc1
CHARACTER SET utf8mb4
collate utf8mb4_unicode_ci;
use gascw_tc1;

CREATE TABLE user(username varchar(15) primary key,
password varchar(15) unique);

insert user values("admin","Gascwtc");
select * from user;

CREATE TABLE student_personal_info(
admission_num varchar(20) primary key,
name varchar(50) not null,
photo longblob null,
father_or_mother_name varchar(50) not null,
nationality_religion_caste varchar(50) not null,
community varchar(50) not null,
gender varchar(20) not null default 'Female',
dob date not null,
dob_in_words varchar(60) not null,
first_language varchar(30) not null,
name_in_tamil varchar(50) not null);

CREATE TABLE academic_info(
admission_num varchar(20) primary key,
roll_no varchar(15) unique not null,
doa date not null,
doa_in_words varchar(50) not null,
academic_year varchar(20) not null,
class_admitted varchar(40) not null,
course_offered_main_and_ancillary varchar(40) not null,
language_under_part_1 varchar(30) not null,
medium_of_instruction varchar(30) not null,
foreign key(admission_num) references student_personal_info(admission_num) on delete cascade);

CREATE TABLE TC_DATA(
admission_num varchar(20) unique not null,
serial_no varchar(25) primary key  not null,
personal_marks_of_identification_1 varchar(50) not null,
personal_marks_of_identification_2 varchar(50) not null,
class_at_leaving varchar(50) not null,
paid_fees varchar(30) not null,
scholarship varchar(50) not null,
medical_inspection varchar(50) not null,
date_on_left_college date not null,
conduct varchar(30) not null,
date_of_TC_applied date not null,
date_of_TC date not null,
class_studied varchar(50) not null,
foreign key(admission_num) references student_personal_info(admission_num) on delete cascade);
