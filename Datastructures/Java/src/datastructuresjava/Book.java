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
public class Book {

    public Book() {
        this.setTitle("");
        this.setAuthor("");
        this.setISBN("");
    }

    public Book(String _title, String _author, String _isbn) {
        this.setTitle(_title);
        this.setAuthor(_author);
        this.setISBN(_isbn);
    }

    private String Title;

    public final String getTitle() {
        return Title;
    }

    public final void setTitle(String value) {
        Title = value;
    }
    private String Author;

    public final String getAuthor() {
        return Author;
    }

    public final void setAuthor(String value) {
        Author = value;
    }
    private String ISBN;

    public final String getISBN() {
        return ISBN;
    }

    public final void setISBN(String value) {
        ISBN = value;
    }

    @Override
    public String toString() {
        return getAuthor() + " - \"" + getTitle() + "\"";
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof Book) {
            Book tjetra = (Book) obj;
            return this.getISBN().equals(tjetra.getISBN());
        }
        return false;
    }
}
