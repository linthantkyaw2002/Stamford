public class BaseCard {
	 // Fields to store details
    protected String cardHolderName;
    protected int cardNumber;
    protected String expiryDate;
    // Default constructor
    public BaseCard() {
        this.cardHolderName = "Unknown";
        this.cardNumber = 0;
        this.expiryDate = "12/30";
    }
    // Overloaded constructor
    public BaseCard(String cardHolderName, String expiryDate, int cardNumber) {
        this.cardHolderName = cardHolderName;
        this.expiryDate = expiryDate;
        this.cardNumber = cardNumber;
    }

    // Methods to get and set card details
    public String getCardHolderName() {
        return cardHolderName;
    }

    public void setCardHolderName(String name) {
        this.cardHolderName = name;
    }

    public int getCardNumber() {
        return cardNumber;
    }

    public String getExpiryDate() {
        return expiryDate;
    }
}