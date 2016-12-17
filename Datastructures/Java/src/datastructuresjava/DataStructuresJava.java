/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package datastructuresjava;

import java.text.SimpleDateFormat;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;

/**
 *
 * @author Ahmet
 */
public class DataStructuresJava {

    private static LibraryDict libDict;
    private static ArrayList<Person> PersonsArrayList;
    private static LinkedList<Person> personsLinkedList;
    private static Person PersonsArray[];
    private static StringBuilder sb;
    private static Person p1, p2, p3, p4, p5;

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        libDict = new LibraryDict();
        HashMap<Person, Book> Library = new java.util.HashMap<>();
        PersonsArray = new Person[3];
        PersonsArrayList = new ArrayList<>();
        sb = new StringBuilder();
        personsLinkedList = new LinkedList<>();

        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        try {
            p1 = new Person("Ahmet", "Murati", "Mashkull", sdf.parse("2013-09-18"));
            p2 = new Person("Ridvan", "Bunjaku", "Mashkull", java.util.Date.from(Instant.now()));
            p3 = new Person("Ridvan", "Aliu", "Mashkull", java.util.Date.from(Instant.now()));
            p4 = new Person("Erzen", "Komoni", "Mashkull", java.util.Date.from(Instant.now()));
            p5 = new Person("Fitim", "Bejtullahu", "Mashkull", java.util.Date.from(Instant.now()));
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
        Book l1 = new Book("Kronikë në gur", "Ismail Kadare", "1233445432");
        Book l2 = new Book("Sikur të isha djalë!", "Haki Stërmilli", "12323212223");

        /**
         * Inicializimi i elementeve të vargut të tipit Array
         */
        for (int i = 0; i < PersonsArray.length; i++) {
            PersonsArray[i] = new Person();
        }

        PersonsArray[0] = p1;
        PersonsArray[1] = p2;
        PersonsArray[2] = p3;
        //PersonsArray[3] = p4;

        Library.put(p1, l2);
        //Biblioteka.Add(p1, l2);
        //Biblioteka.Add(p1, l2);

        sb.append(libDict.AssingBook(p1, l1)).append("\n");
        sb.append(libDict.AssingBook(p1, l1)).append("\n");
        sb.append(libDict.AssingBook(p1, l1)).append("\n");
        sb.append(libDict.AssingBook(p1, l1)).append("\n");

        PersonsArrayList.add(p1);
        PersonsArrayList.add(p2);
        PersonsArrayList.add(p3);
        PersonsArrayList.add(p4);
        PersonsArrayList.add(p5);

        StringBuilder sb2 = new StringBuilder();
        sb2.append("\r\n");
        sb2.append("First element").append("\n");
        personsLinkedList.addFirst(p5);
        personsLinkedList.stream().forEach((p3a) -> {
            sb2.append(p3a.toString()).append("n");
        });
        sb2.append("\r\n").append("\r\n");
        sb2.append("Second element\n");
        personsLinkedList.addFirst(p3);
        personsLinkedList.stream().forEach((p3a) -> {
            sb2.append(p3a.toString());
        });
        sb2.append("\r\n").append("\r\n");
        sb2.append("Third element\n");
        personsLinkedList.addFirst(p2);
        personsLinkedList.stream().forEach((p3a) -> {
            sb2.append(p3a.toString()).append("\n");
        });
        sb2.append("\r\n").append("\r\n");
        sb2.append("Fourth element\n");
        personsLinkedList.add(personsLinkedList.size(), p1);
        sb2.append("\n");
        personsLinkedList.stream().forEach((p3a) -> {
            sb2.append(p3a.toString()).append("\n");
        });

        sb.append("\n\n").append(sb2.toString());
        System.out.println(sb.toString());

    }

}
