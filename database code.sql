-- Create database
CREATE DATABASE LoanEligibilitySystem;

-- Use the database
USE LoanEligibilitySystem;

-- Create table for customer information
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Age INT NOT NULL,
    Gender VARCHAR(10),
    Income DECIMAL(10,2) NOT NULL,
    CreditScore INT NOT NULL,
    LoanAmount DECIMAL(10,2) NOT NULL,
    LoanTerm INT NOT NULL,
    ExistingDebt DECIMAL(10,2) DEFAULT 0,
    EmploymentStatus VARCHAR(50),
    EligibilityStatus VARCHAR(20),
    MobileNumber DECIMAL(10,2) NOT NULL,
    ApplicationDate DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create table for loan products
CREATE TABLE LoanProducts (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    ProductName VARCHAR(100) NOT NULL,
    MinIncome DECIMAL(10,2) NOT NULL,
    MinCreditScore INT NOT NULL,
    MaxDebtToIncome DECIMAL(5,2) NOT NULL,
    MaxLoanAmount DECIMAL(10,2) NOT NULL,
    AvailableTerms VARCHAR(100) NOT NULL
);
