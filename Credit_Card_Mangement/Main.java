// Main.java
import javax.swing.JOptionPane;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        // Predefined credit card objects
        CreditCard[] cards = {
            new CreditCard("John Doe", "12/30", 0, 222222222),
            new CreditCard("Jane Smith", "11/29", 1000, 333333333),
            new CreditCard("Bruce Wayne", "10/28", 25000, 444444444)
        };
      
        // Contact number linked with card holder
        String[][] cardHolderInfo = {
            {"John Doe", "0912345678"},
            {"Jane Smith", "0811112222"},
            {"Bruce Wayne", "0999999999"}
        };

        CreditCard loggedInCard = null;

        // User login using name and card number
        while (loggedInCard == null) {
            try {
                String inputName = JOptionPane.showInputDialog(null, "Enter Card Holder Name:");
                String inputNumberStr = JOptionPane.showInputDialog(null, "Enter Card Number:");

                if (inputName == null || inputNumberStr == null) {
                    JOptionPane.showMessageDialog(null, "Login cancelled. Exiting...");
                    System.exit(0);
                }

                int inputNumber = Integer.parseInt(inputNumberStr.trim());

                for (CreditCard card : cards) {
                    if (card.getCardHolderName().trim().equalsIgnoreCase(inputName.trim()) &&
                        card.getCardNumber() == inputNumber) {
                        loggedInCard = card;
                        break;
                    }
                }

                if (loggedInCard != null) {
                    JOptionPane.showMessageDialog(null, "Login successful!");
                } else {
                    JOptionPane.showMessageDialog(null, "Invalid cardholder name or card number. Please try again.");
                }
            } catch (NumberFormatException e) {
                JOptionPane.showMessageDialog(null, "Invalid input. Card number must be numeric.");
            }
        }
        
        // Menu Loop
        int choice;
        do {
            System.out.println("\n--- Credit Card Menu ---");
            System.out.println("1. Show Card Details");
            System.out.println("2. Make Purchase");
            System.out.println("3. Lock Card");
            System.out.println("4. Unlock Card");
            System.out.println("5. View Purchase History");
            System.out.println("6. Exit");
            System.out.println("------------------------");
            System.out.print("Enter your choice: ");
            choice = scanner.nextInt();
            System.out.println("------------------------");

            switch (choice) {
                case 1:
                    for (int i = 0; i < cards.length; i++) {
                        if (cards[i] == loggedInCard) {
                            String contact = cardHolderInfo[i][1];
                            loggedInCard.showCardDetails(contact);
                        }
                    }
                    break;
                case 2:
                    if (loggedInCard.isLocked()) {
                        System.out.println("Transaction failed: Card is locked.");
                    } else {
                        System.out.print("Enter purchase amount: ");
                        double purchase = scanner.nextDouble(); // To Read User Input
                        loggedInCard.makePurchase(purchase);
                    }
                    break;
                case 3:
                    loggedInCard.lock();
                    break;
                case 4:
                    loggedInCard.unlock();
                    break;
                case 5:
                    loggedInCard.showPurchaseHistory();
                    break;
                case 6:
                    System.out.println("Exiting...");
                    break;
                default:
                    System.out.println("Invalid choice.");
            }
            System.out.println("-----------------------");

        } while (choice != 6);

        scanner.close();
    }
}