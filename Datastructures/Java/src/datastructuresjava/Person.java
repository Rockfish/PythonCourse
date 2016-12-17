/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package datastructuresjava;

import java.util.Objects;

/**
 *
 * @author Ahmet
 */
public class Person {

    public Person() {
        this.setFirstiname("");
        this.setLastname("");
        this.setSex("");
        this.setBirthday(new java.util.Date());
    }

    public Person(String _firstname, String _lastname, String _sex, java.util.Date  _birthday) {
        super();
        // TODO: Complete member initialization
        this.setFirstiname(_firstname);
        this.setLastname(_lastname);
        this.setSex(_sex);
        this.setBirthday(_birthday);
    }

    private String Firstiname;

    public final String getFirstiname() {
        return Firstiname;
    }

    public final void setFirstiname(String value) {
        Firstiname = value;
    }
    private String Lastname;

    public final String getLastname() {
        return Lastname;
    }

    public final void setLastname(String value) {
        Lastname = value;
    }
    private String Sex;

    public final String getSex() {
        return Sex;
    }

    public final void setSex(String value) {
        Sex = value;
    }
    private java.util.Date Birthday = new java.util.Date();

    public final java.util.Date getBirthday() {
        return Birthday;
    }

    public final void setBirthday(java.util.Date value) {
        Birthday = value;
    }

    @Override
    public String toString() {
        return getFirstiname() + " " + getLastname();
    }

    /**
     *
     * @param obj
     * @return
     */
    @Override
    public boolean equals(Object obj) {
        if (obj instanceof Person) {
            Person tjetra = (Person) obj;
            return this.getFirstiname().equals(tjetra.getFirstiname()) && this.getLastname().equals(tjetra.getLastname());
        }
        return false;
    }

    @Override
    public int hashCode() {
        int hash = 5;
        hash = 17 * hash + Objects.hashCode(this.Firstiname);
        hash = 17 * hash + Objects.hashCode(this.Lastname);
        hash = 17 * hash + Objects.hashCode(this.Sex);
        hash = 17 * hash + Objects.hashCode(this.Birthday);
        return hash;
    }

}
