package com.parse.starter;

public class Complaint {
    private String date;
    private String time;
    private String carPlate;
    private String notes;
    private String fullname;
    private String phoneNumber;

    public Complaint(String date, String time, String carPlate, String notes, String fullname, String phoneNumber){
        this.date = date;
        this.time = time;
        this.carPlate = carPlate;
        this.notes = notes;
        this.fullname = fullname;
        this.phoneNumber = phoneNumber;
    }

    public String getDate(){
        return date;
    }

    public String getTime(){
        return time;
    }
    public String getCarPlate(){
        return carPlate;
    }
    public String getNotes(){
        return notes;
    }
    public String getFullname(){
        return fullname;
    }
    public String getPhoneNumber(){
        return phoneNumber;
    }

    public String toString(){
        return this.notes;
    }

}
