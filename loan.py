import streamlit as st
import mysql.connector
from mysql.connector import Error

# Set page config
st.set_page_config(page_title="Loan Eligibility System", page_icon="🏦", layout="wide")

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='LoanEligibilitySystem',
            user='root',
            password='Anusha@95245',
            auth_plugin='mysql_native_password'
        )
        return connection
    except Error as e:
        st.error(f"Database connection error: {e}")
        return None

# Check eligibility function (same as your original)
def check_eligibility(customer_data):
    eligible = True
    reasons = []
    
    # Rule 1: Age must be between 21 and 65
    if customer_data['age'] < 21 or customer_data['age'] > 65:
        eligible = False
        reasons.append("Age must be between 21 and 65")
    
    # Rule 2: Minimum credit score of 600
    if customer_data['credit_score'] < 600:
        eligible = False
        reasons.append("Minimum credit score of 600 required")
    
    # Rule 3: Debt-to-income ratio less than 40%
    total_debt = customer_data['existing_debt'] + (customer_data['loan_amount'] / customer_data['loan_term'])
    debt_to_income = (total_debt / customer_data['income']) * 100
    if debt_to_income > 40:
        eligible = False
        reasons.append(f"Debt-to-income ratio {debt_to_income:.2f}% exceeds 40% limit")
    
    # Rule 4: Must be employed
    if customer_data['employment_status'].lower() in ['unemployed', 'student']:
        eligible = False
        reasons.append("Must be employed or self-employed")
    
    # Rule 5: Minimum income requirement based on loan amount
    if customer_data['loan_amount'] > 50000 and customer_data['income'] < 5000:
        eligible = False
        reasons.append("Income too low for requested loan amount")
    
    return eligible, reasons

# Save to database function
def save_customer_data(customer_data, is_eligible, reasons):
    connection = get_db_connection()
    if not connection:
        return
        
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO Customers 
        (Name, Age, Gender, Income, CreditScore, LoanAmount, LoanTerm, ExistingDebt, EmploymentStatus, EligibilityStatus,MobileNumber)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        eligibility_status = "Approved" if is_eligible else "Denied"
        
        cursor.execute(query, (
            customer_data['name'],
            customer_data['age'],
            customer_data['gender'],
            customer_data['income'],
            customer_data['credit_score'],
            customer_data['loan_amount'],
            customer_data['loan_term'],
            customer_data['existing_debt'],
            customer_data['employment_status'],
            customer_data['mobile_number']
            eligibility_status
        ))
        
        connection.commit()
        st.success("Your application has been recorded.")
        
    except Error as e:
        st.error(f"Error saving customer data: {e}")
    finally:
        if connection.is_connected():
            connection.close()

# Main app function
def main():
    st.title("🏦 Loan Eligibility System")
    st.markdown("Complete the form below to check your loan eligibility")
    
    with st.form("loan_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=18, max_value=100, step=1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            income = st.number_input("Monthly Income ($)", min_value=0, step=100)
            credit_score = st.slider("Credit Score", 300, 850, 650)
            
        with col2:
            loan_amount = st.number_input("Desired Loan Amount ($)", min_value=0, step=1000)
            loan_term = st.selectbox("Loan Term (months)", [12, 24, 36, 60])
            existing_debt = st.number_input("Existing Monthly Debt Payments ($)", min_value=0, step=100)
            employment_status = st.selectbox(
                "Employment Status",
                ["Employed", "Self-Employed", "Unemployed", "Student"]
            )
            mobile_number= st.number_input("Enter your mobile number",min_value=0, step=10)
        
        submitted = st.form_submit_button("Check Eligibility")
        
        if submitted:
            if not all([name, age, income, credit_score, loan_amount, existing_debt,mobile_number]):
                st.warning("Please fill all required fields")
            else:
                customer_data = {
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'income': income,
                    'credit_score': credit_score,
                    'loan_amount': loan_amount,
                    'loan_term': loan_term,
                    'existing_debt': existing_debt,
                    'employment_status': employment_status,
                    'mobile_number':mobile_number
                }
                
                is_eligible, reasons = check_eligibility(customer_data)
                save_customer_data(customer_data, is_eligible, reasons)
                
                st.divider()
                if is_eligible:
                    st.balloons()
                    st.success("## 🎉 CONGRATULATIONS!")
                    st.success("Based on the information provided, you are **ELIGIBLE** for the loan.")
                else:
                    st.error("## 😔 SORRY!")
                    st.error("Based on the information provided, you are **NOT ELIGIBLE** for the loan.")
                    st.warning("**Reasons:**")
                    for reason in reasons:
                        st.write(f"- {reason}")

if __name__ == "__main__":
    main()
