Part 1

Project setup- In the file /generate_data.py/ lives the code used to generate the files /users.csv/, /merchants.csv/, /ledger.csv/ and /gateway_export.csv/. Following the exact given code, the data was generated using a fixed random seed (seed 42). This output is commited to the repository in the folder titled '/payments_fraud_analytics'. The data generation script relies on relative paths and must be run from within its specific directory. Execute the following commands from the repository root:
 cd payments_fraud_analytics
 python generate_data.ipynb

PART A- Output for this part lives in the file /merchant_workbook.xlsx/. Two tabs in this workbooks have data copy pasted from /ledger.csv/ and /merchant.csv/. Third tab is titled 'merchant_workbook'. A fourth tab titled 'merchant_workbook_pivot_table' is created to use as reference for the calculation of merchant_day_classification. All required outputs as per the question live in the tab titled 'merchant_workbook'.
In the 'merchant_workbook' tab, a column (column E:E) titled 'transaction_date' is added next to the column titled 'transaction_time'. The entries in the new column are the date part of the respective time entry in the 'transaction_time' column.

Columns J:L consist of the entries for 'merchant_name', 'category', 'region' filled using standard VLOOKUP nested in IFNA formula. The lookup value from each of these formula was the 'merchant_id' from the respective transaction's 'merchant_id' (column C:C).

In the range P1:T2, MDR_fee_percentage for each of the payment_methods are listed out. For UPI the value is 0%, highest at 2.0% for Card payments, 1.0% for Netbanking payments and 1.5% for Wallet payments. Using this table (P1:T2), entries of column M:M titled 'MDR_fee' are populated using the HLOOKUP formula and 'payment_method' as lookup value.

High value merchant day entries are in the N:N column titled 'merchant_day_classification'. The formula uses nested IF and AND formula, along with SUMIFS formula to detail the condition required to mark "each transaction "High-Value Merchant Day" when a merchant's daily transaction total (via a pivot table) exceeds INR 5,000 and its region is not "East"". Also in the formula is the condition to highlight transactions where a merchant's daily transaction total (via a pivot table) exceeds INR 1,000 and its region is not "East" by marking it as "Mid-Value Merchant Day". Pivot table used for this formula is in the 'merchant_workbook_pivot_table' tab.

In the range P4:V47, one pivot table details the summarized total values for amount_inr and count of transactions by merchant_id and status. In the range X4:Z45, second pivot table gives the count-vs-count-unique comparison (unique days transacted vs. total transaction count) for all the valid merchant_ids.

PART B- For this part, jupyter notepook titled 'paytm_payments_jupyter_nb.ipynb' is used.
 import pandas as pd
 import sqlite3
Then the database was created with below line of code, initiating the connection and creating the cursor object to help with populating the database
 conn = sqlite3.connect('paytm_payments.db')
 cursor = conn.cursor()
 
The "cursor.executescript("""...""")" code ensures if this cell is rerun, the tables are not duplicated. After building the database framework with the same "cursor.executescript("""...""")" code, csv files were loaded and then using-
 merchants_df.to_sql('...', conn, if_exists='append', index=False)
data from the csv files is inserted in the database in form of SQLite tables, hence making it usable for our queries right there in the jupyter notebook. This allows the visualization of the results of the queries. Index is false to prevent addition of an additional index column.

For the database, table 'merchants' has data from 'merchants.csv' with primary key as 'merchant_id', table 'users' has data from 'users.csv' with primary key as 'user_id', table 'transactions' has data from 'ledger.csv' with primary key as 'transaction_id' and 'user_id' and 'merchant_id' acting as foreign keys.
Queries are run using the code line-
 pd.read_sql(..., conn)
where the query name is the first element in the code.
Queries titled 'query_2', 'query_2_1' and 'query_2_2' gives the chargeback details- 'count of chargebacks', 'total chargeback amount' and a list of 'unique [user_ids] affected'.
Query titled 'query_3' finds the burner accounts added in the data earlier. Used the 'join' query on the 'users' and 'transactions' tables, using 'user_id' as the spine/primary key. To calculate the difference between the signup date and the date of transaction, instead of using 'datediff()' which does not work in SQLite, 'julianday()' was used. The output gives us the 'user_ids' which are the burner acoounts, their respective 'signup_dates', 'transaction_dates', 'status' and the 'time before transaction' in days.
Query titled 'query_4' gives the 8 'user_ids' involved in the velocity attacks, with all 8 buckets of such transactions fully detected. For this the 'transaction_time' metric of all these transactions were divided into 10 minute buckets using the code-
 substr(transaction_time, 1, 15) || '0:00' as time_bucket
which gave us the appropriate 'transaction_time' entries to be able to reliably work with. Then counting transactions for each 'user_id' where 3 or more happened within the 10 minute time frame, by using the 'having' query.
Query titled 'query_5' uses 'left join' query to join 'transactions' and 'merchant' tables with 'merchant_id' as the spine/primary key. Removing the 'chargeback' transactions, we find top 10 'merchant_ids' with the highest total 'amount_inr'. The result also tells the total number of valid transactions by using the query 'distinct'. 
Queries titled 'query_6', 'query_6_1', 'query_6_2' and 'query_6_3' give the top 10 highest spender 'user_ids' based on total 'amount_inr' for all the valid transactions. Queries used are 'order by', 'group by', left join
and 'limit'. Also these queries segregate the 4 'payment_methods' and builds the list of top 10 spender 'user_ids' for each of these separately.

PART C- In reconcile.ipynb, 2 dataframes 'ledger_df' and 'gateway_df' are used. set() function creates unique sets of ids from each dataframe. Create 2 variables with unique 'transaction_ids' for both the data frames by using '.isin()' and '.copy()' functions.

For 'amount_inr' and 'status' mismatch we use '.intersection()' function between 'ledger_ids' and 'gateway_ids'. This gives us the dataframe to use with the common ids from both the 'ledger_df' and 'gateway_df' to create the 'merged_df' dataframe for actual calculations. Function used- '.merge()'. Merge happens with 'transaction_id' as spine and uses '_ledge' and '_gate' suffixes to mark same titled columns from both the data frames (like 'amount_inr_ledg' and 'amount_inr_gate' and 'status_ledg' and 'status_gate').

The variable 'desired_columns' helps assort the dataframe in the order that makes the data more readable. Using merged_df['amount_inr_ledg']-merged_df['amount_inr_gate'] we get the difference of 'amount_inr' from both the columns ('amount_inr_ledg' and 'amount_inr_gate') and find which common 'transaction_ids' have the differences. Function 'if' is used to find total discrepancy for all the transactions where the difference is not 0. Similarly for status mismatch we use 'merged_df[merged_df['status_ledg']!=merged_df['status_gate']].copy()' inorder to find the mismatches in transaction status for the common 'transaction_ids'.

For the deliverable Reusable Reconciliation Function, def and return functions are used to build 'reconcile_payments(ledger_df, gateway_df)'. Since def is a closed environment function, the already tested codes are rerun and get the required results, which are consistent with the ~5%/~3%/~2%/~2% injection rates in generate_data.py.
Running the sets of code before the def block gives validity to the logic behind these merge and calculation codes.

PART D- The deliverables for this part are the /analytics_dash.ipynb/ file, /headline_scorecards.png/, /trend_layer_chart.png/, /breakdown_gmv_layer.png/ and /details_layer_table.png/. 'ledger', 'gateway' and 'merchants' csvs are inerted as dataframes.For the purpose of plotting and visualization of the data tables and charts, following codes are used-
 import pandas as pd
 import numpy as np
 import matplotlib.pyplot as plt
 import matplotlib.ticker as ticker
 from datetime import datetime, timedelta
 import seaborn as sns
matplotlip.ticker helps convert raw numbers in the dataframe to desired unit likr INR with ',' delimiters for 1000s, 10,00,000s etc currency values. Loops are also used to run the conditional formatting logic in the table visual. Table is visualized in the plot with 'matplotlib.pyplot.table'. Images are downloaded with 'plt.savefig('...',dpi=300)'

'headline_scorecard'- To find the GMV 'Gross Merchandise Value', variable for all successful transactions from ledger_df are used. For the overall success rate successful transactions are proportioned against total transactions, for reconciliation match rate same as part C calculate number of common 'transaction_ids' and then calculate proportion with total transactions. For chargeback ratio, similar calculations using .status==() function to filter out chargeback transactions. Reconciliation match rate being below 100% shows significant issues in the 'gateway_export' report. Overall Success rate is also significantly below 95%, calling for a thorough analysis of merchants with lower success rate. Chargeback ratio is also significant, will need a merchant wise breakdown of the chargeback transactions proportionate to total transactions.

'trend_layer_chart'- A line chart tracking Daily GMV across 30-day timelapse, side-by-side the Daily Chargebacks count gives a good view at how these two metrics moved in this window. Although the GMV moved more or less linearly over the window, the chargeback va;ue moves a bit more eratically. Spikes at around the 13th, 21th and the 28th of Jan lead to steady increase in chargebacks, even as total GMV moves more predictably. The twin axis method was chosen to simply map the rate of movement of these metrics not correlate their actual values with each other. The negative Y-axis value approach was made to ensure that the entire line and the data points are fully rendered in the chart area without cutting off. Cumulative value is used for this chart to ensure trends can be more vividly followed without the distraction of slow days (lesser transactions).

'breakdown_gmv_layer'- Stacked bar chart showing GMV for all the different merchant 'categories', across 4 different 'payment_methods'. Bar chart is the perfect visual for this task as it gives the fastest visual for anyone wanting to find exactly which 'category' sees most traffic and which 'payment_method' dominates the landscape. Its easy to spot the UPI taking the most space for each and every 'category'. Proportion for UPI is considerably more than 50% for 'travel', 'grocery', 'bill_payment' and 'recharge', with majority shaare in other categories as well. 2nd most used 'payment_method' is the Wallet, but interestingly only other 'payment_method' being used for 'recharge' 'category' apart from UPI seems to be the 'Netbankink' method. Also 'Netbanking' is also a famous option for 'ecommerce' category, more so than 'food_delivery', 'entertainment', 'bill_payment'.

'details_layer_table'- Top 10 merchants by total transactions with merchants highlighted if chargeback ratio is more than 1%. For all but 3 merchants the chargeback ratio was more than 1%. This corroborates with findings of the headline and trend layers. Average chargeback ratio stays near 5-6% except for two outliers with the ratio reaching 16-19% for these merchants. This could be seen as a base for added caution for these merchants, despite being high traffic merchants, they have higher than usual cgargeback ratios. As for the three merchants with 0 chargeback ratios, metrics are a positive sign. For this visual, simple table layout was chosen and the merchants with chargeback ratio more than 1% had the entire row hilighted in light red, with the data text color changed to dark red to hilight these merchants' entries from the others.Merchants are arranged in descending order of 'Total Transactions', making the comparisons that much easier.



---



Part 2

Project Setup- Part 2 lives in a seperate folder in the same repository as Part 1, titled- /credit_risk_lending_ml/. To create the database to be used in this part we run the code provided in the question itself in juoyter notebook titled 'generate_data.py'. It creates two datasets titled- 'credit_applicants.csv' and 'txn_behaviour.csv'. These are datasets for applicant credit scores and transaction behaviours respectivly. Same as part 1, fixed random seed 42 was used to generate the datasets.

PART A- For the calculations in this and Parts B and C, script was written and run in jupyter notebook titled 'credit_risk_modeling.ipynb'. For the purpose of running the codes for this and subsequent parts, following libraries were installed-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import (roc_auc_score, accuracy_score, precision_score, recall_score,
     f1_score, confusion_matrix, classification_report, ConfusionMatrixDisplay, RocCurveDisplay)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import IsolationForest
Handling the Thin-File Strategy: To address the 80 applicants missing a credit bureau score, we engineered an is_thin_file boolean flag directly from the raw data before any imputation occurred to preserve this behavioral attribute. Crucially, no rows were dropped from the dataset. Next, a stratified train/test split was performed on the default column (which has a 20% baseline rate) using random_state=42 to ensure defaulters were evenly distributed.
Finally, to prevent data leakage, the median credit_bureau_score was calculated using only the training data, and then applied to populate the NaN values in both the Test and Train sets (adhering to the fit-on-train-only rule). For categorical variables, One-Hot Encoding was utilized to create dummy columns with binary entries (0 or 1).

PART B- Logistic regressiona nd desicion tree classifier methods used on dataset from  to train identical scaled train/test data, that was first scaled for the benifit of the ML model. Evaluated both models with a confusion matrix, accuracy, precision, recall, F1, and ROC curve + AUC, presented side by side in a comparison table. The result is printed in the notebook and generated in the form of two image titled 'confusion_matrix_charts.png' (confusion matrix comparison) and 'model_side-by-side_comparison.png' (accuracy, precision, recall, F1, and ROC curve + AUC comparison). Risk based pricing of loan interests for 4 equally ssized risk categories built via logistic regression is also in image format titled "risk_based_pricing_table.png".

PART C- Using isolationForest method on the scaled dataset consisting of only numeric features from the source 'txn_behaviour.csv' file to run the ML model and try and find all 15 injected anomalies. The model was able to flag 11 correct anomalies, and 4 normal entries erroneously tagged as anomalies.
For the optional k-means clustering exercise, both elbow and CH index methods were used and results compared. Two behavioural clustering was compared, k=2 and k=5, with k=5 yeilding more effective results reflecting the reality of 'is_thin_file' category applicants who were not high default risk applicants.  The ressultss are saved in an image file titled 'kmeans_evaluation_charts.png'.

PART D- In the txn_behaviour.csv and credit_applicants.csv datasets, there are no explicit personal identifiers like gender or location. In spite of this, the features present can still introduce bias by acting as proxies for protected attributes in a real-world deployment.

Suspected Feature 1- 'monthly_income_inr' This feature could exclude lower salaried individuals from unbiased loan access. Due to the systemic gender pay gap across similar age brackets and employment types, penalizing lower income inherently acts as a proxy penalty against female applicants.
Suspected Feature 2- 'employment_type' This feature can act as a proxy for an applicant's location of origin/brth. Gig workers are majorly from tier 3 or rural cities moving to metros or tier 1-2 cities. If the model pushes the narrative that gig workers are more prone to defaults, then it will automatically be more biased towards people from tier 2,3 cities/rural region.
Suspected Feature 3- 'credit_bureau_score' As is more probable for families from rural regions of the country, females manage a vast majority of the family finances. But in official credit documents from banks/fintechs, eldest male of the family is named. This inherently creates a bias against the female applicants simply because even if their data made it into the dataset, their absent/lower credit_bureau_score makes them more likely to be denied a loan by an automated system.

Some governance steps to tackle these biases- 
A maker-checker human-in-the-loop review for any applicant flagged for decline who possesses a low monthly_income_inr but a comparatively healthy upi_monthly_inflow_inr should be routed to a human underwriter to verify actual cash flow.
A maker-checker human-in-the-loop that manually review applicants falling into high-risk, high-interest behavioral clusters who are also flagged as is_thin_file to ensure marginalized, unbanked demographics are not being systematically auto-declined without secondary evaluation.

### Final Model Comparison

| Model | Accuracy | Precision | Recall | F1 Score | ROC AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | 0.76 | 0.3889 | 0.35 | 0.3684 | 0.7188 |
| **Decision Tree** | 0.65 | 0.2222 | 0.30 | 0.2553 | 0.5188 |
| **Isolation Forest (Anomaly)** | - | - | 11 / 15 (73.3%) | - | - |

I recommend deploying the Logistic Regression model for the Paytm Postpaid product. It achieved a superior ROC AUC of [0.7188] compared to the Decision Tree's [0.5188], indicating a stronger overall mathematical ability to distinguish between legitimate borrowers and potential defaulters. Furthermore, Logistic Regression outputs continuous, reliable predicted probabilities, which successfully enabled the creation of our strict, 4-tier monotonic risk-based pricing framework (allowing us to assign lower rates to safer segments). Finally, for a highly regulated financial product like Postpaid, Logistic Regression provides clear, linear explainability to regulators and auditors, making it much easier to monitor for the proxy biases identified in our governance review.



---



Part 3

Project Setup- All scripts in this module were executed using the strictly deterministic, rule-based baseline mode (MOCK_LLM=1). No external network calls or LLM API keys were utilized, ensuring fully reproducible grading against the prescribed mathematical and logical constraints.

Advisory Agent Transcripts (advisory_agent.py)

--- RUNNING ADVISORY AGENT (MOCK_LLM=1) ---

[INV01] Status: AUTO_FINALIZED
For Conservative investor INV01, we recommend an allocation across ['PAYBOND', 'PAYGOLD', 'PAYRETAIL'] with an expected portfolio return of 9.2% and volatility of 8.4%.
-----------------------------------------------------------------
[INV02] Status: AUTO_FINALIZED
For Moderate investor INV02, we recommend an allocation across ['PAYRETAIL', 'PAYINFRA', 'PAYGOLD'] with an expected portfolio return of 11.3% and volatility of 12.6%.
-----------------------------------------------------------------
[INV03] Status: ESCALATED_TO_HUMAN_ADVISOR
FLAG: ESCALATED_TO_HUMAN_ADVISOR - Computed portfolio std dev (20.58%) exceeds 20% safety limit.
-----------------------------------------------------------------
[INV04] Status: AUTO_FINALIZED
For Moderate investor INV04, we recommend an allocation across ['PAYRETAIL', 'PAYINFRA', 'PAYGOLD'] with an expected portfolio return of 11.3% and volatility of 12.6%.
-----------------------------------------------------------------
[INV05] Status: ESCALATED_TO_HUMAN_ADVISOR
FLAG: ESCALATED_TO_HUMAN_ADVISOR - Computed portfolio std dev (20.58%) exceeds 20% safety limit.
-----------------------------------------------------------------

Structured Disclosure Extraction (extract_disclosure.py)

--- RUNNING DISCLOSURE EXTRACTION (MOCK_LLM=1) ---

[doc_01] Extraction Result:
{'risk_flags': [], 'hedging_detected': True, 'sentiment': 'cautious'}
--------------------------------------------------
[doc_02] Extraction Result:
{'risk_flags': ['litigation'], 'hedging_detected': False, 'sentiment': 'neutral'}
--------------------------------------------------
[doc_03] Extraction Result:
{'risk_flags': ['customer concentration'], 'hedging_detected': False, 'sentiment': 'neutral'}
--------------------------------------------------
[doc_04] Extraction Result:
{'risk_flags': [], 'hedging_detected': True, 'sentiment': 'cautious'}
--------------------------------------------------
[doc_05] Extraction Result:
{'risk_flags': [], 'hedging_detected': False, 'sentiment': 'confident'}
--------------------------------------------------
[doc_06] Extraction Result:
{'risk_flags': ['regulatory'], 'hedging_detected': False, 'sentiment': 'neutral'}
--------------------------------------------------

Multi-Agent Debate Demo (debate.py)

--- RUNNING 3-AGENT DEBATE FOR PAYTECH (MOCK_LLM=1) ---

BULL AGENT: With an impressive analyst expected return of 19.0% against a beta of 1.55, PAYTECH offers highly attractive upside potential. The growth trajectory easily justifies the allocation.

BEAR AGENT: I strongly disagree. A standard deviation of 34.0% indicates excessive, dangerous volatility. Holding PAYTECH introduces far too much uncompensated risk to a stable portfolio under current market conditions.

SYNTHESIZER AGENT: This debate highlights a classic high-risk, high-reward dynamic. While the Bull correctly identifies the compelling 19.0% expected return, the Bear is right to flag the severe 34.0% volatility. Recommendation: Permit allocation only for Aggressive risk profiles, with strict position sizing.
-----------------------------------------------------------------

DCF Valuation & Sensitivity Analysis (dcf_calculator.py)

--- SENSITIVITY TABLE: IMPLIED EV (Millions INR) ---
              TG: 3.0%  TG: 4.0%  TG: 5.0%
WACC: 11.97%  ₹4538.1M  ₹4969.4M  ₹5524.4M
WACC: 12.97%  ₹4061.1M  ₹4393.8M  ₹4810.1M
WACC: 13.97%  ₹3671.8M  ₹3934.4M  ₹4255.6M

DCF vs. EV/EBITDA Cross-Check:
The implied Enterprise Value from our DCF model (₹4,393.84M) came in lower than our simple EV/EBITDA cross-check (₹6,000.00M at a 10x multiple). This discrepancy is expected, as our DCF utilizes a conservative 12.97% WACC and heavily penalizes the cash flows in the terminal year to maintain a safe 8.97% spread against our terminal growth rate. The 10x EBITDA multiple reflects a more optimistic broader market sentiment that has not been explicitly risk-adjusted for PAYFIN's specific 1.35 beta.
