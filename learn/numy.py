import numpy as np
import time

# =============================================================================
# DAY 1: NUMPY MASTERY - INTERVIEW PREPARATION CHALLENGES
# Complete all 5 challenges. Time yourself on each one.
# =============================================================================

print("🚀 NUMPY MASTERY - DAY 1 CHALLENGES")
print("=" * 50)

# CHALLENGE 1: ARRAY OPERATIONS (5 minutes)
# You're analyzing sales data. Given daily sales for 30 days:
print("\n📊 CHALLENGE 1: Sales Performance Analysis")
print("-" * 40)

np.random.seed(42)
daily_sales = np.random.randint(1000, 5000, 30)
print(f"Daily sales (30 days): {daily_sales[:10]}...") # showing first 10

# TODO: Complete these tasks
print("\nYour tasks:")
print("1. Find days with sales > average + 1 standard deviation")
print("2. Calculate 7-day moving average")
print("3. Find the longest streak of increasing sales")

# YOUR CODE HERE:
# Task 1:
avg_sales = np.mean(daily_sales)
std_sales = np.std(daily_sales)
high_performance_days = daily_sales > (avg_sales + std_sales)
print("TASK 1")
print("Number of high-performance days in a month are:", np.count_nonzero(high_performance_days))

# Task 2:
print(daily_sales[0:7])
moving_avg_7day = []
for index_tuple, each_day in np.ndenumerate(daily_sales):
    index = index_tuple[0]
    if index > 5:
        avg_7day = sum(daily_sales[index-6:index])/7
        moving_avg_7day.append(float(avg_7day))
print("TASK 2")
print("7 - day moving averages starting from 7th day of the month to the end are \n", moving_avg_7day)

# Task 3:
def longest_increasing_streak(arr):
    print("TAsK 3")
    sales_array =arr
    longest_streak=0
    checking_index=0
    inner_index =0
    length_of_sales_array= len(sales_array)
    for index_tuple, each_day in np.ndenumerate(sales_array):
        count=0
        starting_day=checking_index
        cheking_array = sales_array[starting_day:]
        for index_tuple, each_sale in np.ndenumerate(cheking_array):
            inner_index=index_tuple[0]
            if (starting_day+1) >= length_of_sales_array:
                break
            if cheking_array[inner_index+1] > each_sale:
                count=count+1
            else:
                checking_index = inner_index + 1 + starting_day
                break
        if checking_index > len(sales_array) or (starting_day+1) >= length_of_sales_array:
            break
        if count>longest_streak:
            longest_streak = count
    print("longest streak is", longest_streak)
    pass

longest_increasing_streak(daily_sales)



# =============================================================================

# CHALLENGE 2: MATRIX OPERATIONS (7 minutes)
# You're working with customer transaction data
print("\n💳 CHALLENGE 2: Customer Transaction Matrix")
print("-" * 40)

# Customer-Product purchase matrix (10 customers, 5 products)
np.random.seed(42)
purchases = np.random.randint(0, 50, (10, 5))
product_names = ['Laptop', 'Phone', 'Tablet', 'Watch', 'Headphones']
print("Purchase matrix (customers x products):")
print(purchases)  # showing first 3 customers

# TODO: Complete these business questions
print("\nBusiness Questions:")
print("1. Which customer spent the most money?")
print("2. Which product has highest total sales?")
print("3. Create a normalized matrix (customer spending as % of their total)")

# YOUR CODE HERE:
# Assume prices: [1000, 800, 600, 400, 200]
prices = np.array([1000, 800, 600, 400, 200])

# Task 1: Customer total spending
print('\nTASK 1')
highest_amount =0 
customer = 1
for quantity in purchases:
    amount_spend = quantity*prices
    total_amount_spent = sum(amount_spend)
    if total_amount_spent>highest_amount:
        highest_amount = total_amount_spent
        rich_customer = customer
    customer += 1
print('rich customer is',rich_customer,'th cusotmer with amount spent around',highest_amount)


# Task 2: Product total sales
print('TASK 2')
amount_spend  = purchases*prices
amount_spend = list(zip(*amount_spend))
highestsales = 0
productindex=0
for each_product in amount_spend:
    totalsales= sum(each_product)
    if totalsales > highestsales:
        highestsales = totalsales
        trendingproduct = productindex
    productindex +=1
    
print("Product with highest sales is",product_names[trendingproduct])

# Task 3: Normalized matrix
#normalized_purchases = # COMPLETE THIS
print('TASK 3')
normalized_purchases=list()
for quantity in purchases:
    amount_spend = quantity*prices
    total_amount_spent = np.sum(amount_spend)
    percentage_amount = (amount_spend * 100) / total_amount_spent
    normalized_purchases.append(percentage_amount)
normalized_purchases = np.array(normalized_purchases)
print(normalized_purchases)


# CHALLENGE 3: BOOLEAN INDEXING & FILTERING (6 minutes)
# A/B Testing scenario - very common in interviews!
print("\n🧪 CHALLENGE 3: A/B Test Analysis")
print("-" * 40)

# Simulation: 1000 users, random assignment to A/B test
np.random.seed(42)
n_users = 1000
test_group = np.random.choice(['A', 'B'], n_users)
conversion_rates = {'A': 0.12, 'B': 0.15}  # B is better
conversions = np.array([np.random.random() < conversion_rates[group] 
                       for group in test_group])

print(f"Users in group A: {np.sum(test_group == 'A')}")
print(f"Users in group B: {np.sum(test_group == 'B')}")

# TODO: Analyze the test results
print("\nAnalysis tasks:")
print("1. Calculate conversion rate for each group")
print("2. Find users who converted in group B but would not have in group A")
print("3. Calculate statistical significance (basic version)")

# YOUR CODE HERE:
# Task 1:

print("TASK 1")
unique_values = np.unique(test_group)
conversionRate = {}
for eachUniqueValue in unique_values:
    numberOfUsers = np.sum(test_group == eachUniqueValue)
    if eachUniqueValue in conversion_rates:
        totalConversionRate = numberOfUsers * (conversion_rates[eachUniqueValue])
        conversionRate['conversion_rate_'+str(eachUniqueValue)] = float(totalConversionRate)

for key,value in conversionRate.items():
    print(key,':',value)

# Task 2:
#group_b_indices = # COMPLETE THIS
#group_b_conversions = # COMPLETE THIS

print('TASK 2')
print(conversions)
bcount =0 
group_b_indices = []
for index, eachValue in np.ndenumerate(test_group):
    if eachValue == 'B':
        group_b_indices.append(index)
        bcount +=1

print(group_b_indices)








