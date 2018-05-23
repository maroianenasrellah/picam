public class Book { 
String title; 
boolean borrowed; 
// Creates a new Book 
public Book(String bookTitle){ 
    bookTitle= "The Da Vinci Code";
} 
// Marks the book as rented 
public void borrowed() { 
    int borrowed= 1;
    // Implement this method 
} 
// Marks the book as not rented 
public void returned() { 
    int returned = 2;
    // Implement this method 
} 
// Returns true if the book is rented, false otherwise 
public boolean isBorrowed(int returned, int borrowed) { 
    if (borrowed < 2 )
    return true;
    else 
    return false;
    // Implement this method 
} 
// Returns the title of the book 
public String getTitle() { 
    String bookTitle= "The Da Vinci Code";
    return bookTitle;
    // Implement this method 
}

public static void main(String[] arguments){ 
    // Small test of the Book class
    int returned= 1;
    int borrowed= 2;
    Book example = new Book("The Da Vinci Code"); 
    System.out.println("Title (should be The Da Vinci Code): " +example.getTitle()); 
    System.out.println("Borrowed? (should be false): " + example.isBorrowed(returned, borrowed)); 
    example.borrowed(); 
    System.out.println("Borrowed? (should be true): " + example.isBorrowed(returned, borrowed)); // should be returning true but it not. It printing false
    example.returned(); 
    System.out.println("Borrowed? (should be false): " + example.isBorrowed(returned, borrowed)); 
}