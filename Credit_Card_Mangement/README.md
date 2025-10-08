# 🧾 Credit Card Management System (Console Version)

## 📘 Overview
This project is a **console-based Credit Card Management System** written in **Java**.  
It demonstrates **object-oriented programming (OOP)** principles such as **inheritance**, **encapsulation**, and **polymorphism**, while managing basic credit card operations without any graphical user interface (GUI) or database.

All input and output interactions are done via the **command line**.  
Data is stored **in memory** during runtime using Java objects.

---

## 🧩 Features
- Create and manage credit card accounts  
- Store cardholder details and card limits  
- Display card information  
- Perform balance updates and credit limit checks  
- Demonstrate inheritance between base and derived classes  
- Purely console-based (no GUI or database dependency)

---

## 🏗️ Class Structure

### 1. BaseCard.java
- Acts as the **parent class** for all types of cards.  
- Contains **common attributes** such as:
  - `cardNumber`
  - `cardHolderName`
  - `creditLimit`
  - `balance`
- Provides basic **getter/setter methods** and **display functionality**.

### 2. CreditCard.java
- Inherits from `BaseCard`.
- Adds **specific features** such as:
  - `interestRate`
  - `cardType` (e.g., Gold, Silver, Platinum)
- Includes methods to:
  - Make purchases and adjust balance
  - Calculate remaining credit
  - Apply interest or fees

### 3. Main.java
- Acts as the **driver class**.
- Provides a simple **text-based menu** for user interaction:
  - Create a new credit card
  - View all cards
  - Make a purchase
  - Show balance and available credit
  - Exit the program

---

## ⚙️ How to Compile and Run

### Compile
```bash
javac BaseCard.java CreditCard.java Main.java
```

### Run
```bash
java Main
```

Make sure all `.java` files are in the **same directory** before compiling.

---

## 💻 Example Output
```
===== Credit Card Management System =====
1. Create New Card
2. View Card Info
3. Make Purchase
4. Exit
Enter choice: 1

Enter cardholder name: Bruce Wayne
Enter card number: 123456789
Enter credit limit: 10000
Enter interest rate: 2.5
Card created successfully!

Enter choice: 3
Enter amount to purchase: 2500
Purchase successful. Remaining credit: 7500.0

Enter choice: 2
Cardholder: Bruce Wayne
Card Number: 123456789
Balance: 2500.0
Credit Limit: 10000.0
Interest Rate: 2.5%

Enter choice: 4
Exiting program...
```

---

## 🧠 Concepts Demonstrated
- Class inheritance (`BaseCard` → `CreditCard`)
- Method overriding and encapsulation
- Console I/O using `Scanner`
- Object management in memory
- Basic control flow (loops, conditionals, menu systems)

---

## 🧑‍💻 Author
**Lin Thant Kyaw**  
IT Student – Stamford International University  
GitHub: [your-github-username]

---

## 📄 License
This project is open-source and free for educational use.
