  
drop database if exists "vms";
create database "vms" with encoding = 'UTF8';
drop user if exists vms_user;
create user vms_user with password 'vm5_u53r';
grant all privileges on schema public to vms_user
