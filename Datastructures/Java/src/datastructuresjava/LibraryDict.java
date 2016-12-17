/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package datastructuresjava;

/**
 *
 * @author Ahmet
 */
public class LibraryDict extends java.util.HashMap<Person, Book> {

    public final boolean AddLending(Person p, Book b) {
        Book l2 = new Book();

        boolean res = this.TryGetValue(p, b);
        l2 = b;
        res = b.equals(l2);
        if (!res) {
            this.put(p, b);
            res = true;
        } else {
            res = false;
        }
        return res;
    }

    private boolean TryGetValue(Person p, Book b) {
        boolean res =false;
        for (int i = 0; i < this.size(); i++) {
            if(!p.equals(this.get(i))){
            
            } else {
                res =true;
                break;
            }
          
        }
        return res;
    }
    

		

    public final String AssingBook(Person p, Book b) {
        String str = ("Trying to assing the book " + b.toString() + " to the person " + p.toString());
        if (this.AddLending(p, b)) {
            str += ("\nThe book " + b.toString() + " is assigned to the person " + p.toString());
        } else {
            str += ("\nThe book " + b.toString() + " is not assigned to the person " + p.toString());
        }
        return (str);
    }

}
