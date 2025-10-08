// CreditCard.java
import java.util.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

// CreditCard class extends BaseCard with more functionality 
public class CreditCard extends BaseCard {
    private int cvv;
    private double balance;
    private static final double MAX_CREDIT_LIMIT = 50000;
    private boolean isLocked;
    private List<String> purchaseHistory = new ArrayList<>();

    private String[][] historyArray = new String[10][2];
    private int historyIndex = 0;

    private int points = 0;  // Added points field to track reward points

    // Default constructor
    public CreditCard() {
        super();
        this.cvv = generateCVV();
        this.balance = 0.0;
        this.isLocked = true;
    }
    
    // Overloaded constructor
    public CreditCard(String cardHolderName, String expiryDate, double balance, int cardNumber) {
        super(cardHolderName, expiryDate, cardNumber);
        this.cvv = generateCVV();
        this.balance = balance;
        this.isLocked = false;
    }

    private int generateCVV() {
        Random rand = new Random();
        return 100 + rand.nextInt(900); // Generates a random 3-digit
    }

    public int getCVV() {
        return cvv;
    }

    public double getBalance() {
        return balance;
    }

    public void lock() {
        isLocked = true;
        System.out.println("Card is now locked.");
    }

    public void unlock() {
        isLocked = false;
        System.out.println("Card is now unlocked.");
    }

    public boolean isLocked() {
        return isLocked;
    }
    
    // Handles purchase logic, updates balance and history
    public boolean makePurchase(double amount) {
        if (amount <= 0) return false;
        if (balance + amount > MAX_CREDIT_LIMIT) {
            System.out.println("Transaction declined: Over credit limit.");
            return false;
        }
        
        balance += amount;

        // Calculate points: 1 point for every 100 spent
        int earnedPoints = (int) Math.floor(amount / 100);
        points += earnedPoints;

        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        purchaseHistory.add("Purchased: $" + amount + " on " + timestamp);

        // Store in 2D array for table format display
        if (historyIndex < historyArray.length) {
            historyArray[historyIndex][0] = "$" + amount;
            historyArray[historyIndex][1] = timestamp;
            historyIndex++;
        }

        System.out.println("Purchase successful. New balance: " + balance);
        System.out.println("You earned " + earnedPoints + " point(s). Total points: " + points); // Display points earned and total
        return true;
    }
    
    // Displays card details
    public void showCardDetails(String contactNumber) {
        System.out.println("Card Holder: " + cardHolderName);
        System.out.println("Contact Number: " + contactNumber);
        System.out.println("Card Number: " + cardNumber);
        System.out.println("Expiry Date: " + expiryDate);
        System.out.println("Current Balance: " + balance);
        System.out.println("Reward Points: " + points);  // Display current points
    }

    // Displays purchase history
    public void showPurchaseHistory() {
        System.out.println("---- Purchase History (Table Format) ----");

        if (historyIndex == 0) {
            System.out.println("No purchases yet.");
        } else {
            System.out.println("No.  | Amount        | Timestamp");
            System.out.println("----------------------------------------------");

            for (int i = 0; i < historyIndex; i++) {
                String no = String.valueOf(i + 1);
                String amount = historyArray[i][0];
                String time = historyArray[i][1];

                while (no.length() < 4) no += " ";
                while (amount.length() < 13) amount += " ";

                System.out.println(no + "| " + amount + "| " + time);
            }
        }

        System.out.println("----------------------------------------------");
    }
}