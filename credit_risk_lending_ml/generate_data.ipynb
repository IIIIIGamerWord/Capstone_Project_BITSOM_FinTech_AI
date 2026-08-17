{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "967a7246-597f-4f97-bdb7-a33942a817cd",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "93631876-8770-4428-b091-232d6e79fb21",
   "metadata": {
    "editable": true,
    "slideshow": {
     "slide_type": ""
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "np.random.seed(42)\n",
    "N = 400\n",
    "\n",
    "age = np.random.randint(21, 60, N)\n",
    "monthly_income_inr = np.random.randint(15000, 150000, N)\n",
    "existing_loans_count = np.random.randint(0, 5, N)\n",
    "credit_utilization_ratio = np.round(np.random.uniform(0.05, 0.95, N), 2)\n",
    "upi_monthly_inflow_inr = np.random.randint(2000, 120000, N)\n",
    "bounced_payments_count = np.random.poisson(1.2, N)\n",
    "employment_type = np.random.choice([\"salaried\", \"self_employed\", \"gig\"], N,\n",
    "                                    p=[0.55, 0.30, 0.15])\n",
    "credit_bureau_score = np.random.randint(300, 900, N).astype(float)\n",
    "\n",
    "# 20% of applicants are \"new to credit\" (thin-file): no bureau score at all\n",
    "thin_file_idx = np.random.choice(N, size=int(0.20 * N), replace=False)\n",
    "credit_bureau_score[thin_file_idx] = np.nan"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "e3230232-8680-472d-be07-a47614feab2d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# risk score combines income (protective), bounced payments and utilization (risky),\n",
    "# and UPI inflow (protective, alternate-data signal) -- deliberately usable even\n",
    "# when credit_bureau_score is missing\n",
    "z_income = (monthly_income_inr - monthly_income_inr.mean()) / monthly_income_inr.std()\n",
    "z_bounced = (bounced_payments_count - bounced_payments_count.mean()) / (bounced_payments_count.std() + 1e-9)\n",
    "z_util = (credit_utilization_ratio - credit_utilization_ratio.mean()) / credit_utilization_ratio.std()\n",
    "z_upi = (upi_monthly_inflow_inr - upi_monthly_inflow_inr.mean()) / upi_monthly_inflow_inr.std()\n",
    "\n",
    "risk_score = -2.25 + (-0.9 * z_income) + (0.8 * z_bounced) + (0.7 * z_util) + (-0.5 * z_upi) + np.random.normal(0, 0.6, N)\n",
    "default_prob = 1 / (1 + np.exp(-risk_score))\n",
    "default = (np.random.uniform(0, 1, N) < default_prob).astype(int)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "3502efe5-3c1d-4646-8dc7-b3700f937129",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "default\n",
      "0    0.7975\n",
      "1    0.2025\n",
      "Name: proportion, dtype: float64\n"
     ]
    }
   ],
   "source": [
    "df = pd.DataFrame({\n",
    "    \"applicant_id\": [f\"APP{1000+i}\" for i in range(N)],\n",
    "    \"age\": age,\n",
    "    \"monthly_income_inr\": monthly_income_inr,\n",
    "    \"existing_loans_count\": existing_loans_count,\n",
    "    \"credit_utilization_ratio\": credit_utilization_ratio,\n",
    "    \"upi_monthly_inflow_inr\": upi_monthly_inflow_inr,\n",
    "    \"bounced_payments_count\": bounced_payments_count,\n",
    "    \"credit_bureau_score\": credit_bureau_score,\n",
    "    \"employment_type\": employment_type,\n",
    "    \"default\": default,\n",
    "})\n",
    "df.to_csv(\"credit_applicants.csv\", index=False)\n",
    "print(df[\"default\"].value_counts(normalize=True))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "55617a84-3ded-432a-a405-c38f06b79297",
   "metadata": {},
   "outputs": [],
   "source": [
    "# --- second dataset: transaction-behaviour rows for anomaly detection ---\n",
    "M = 250\n",
    "behaviour = pd.DataFrame({\n",
    "    \"txn_id\": [f\"BTXN{5000+i}\" for i in range(M)],\n",
    "    \"applicant_id\": np.random.choice(df[\"applicant_id\"], M),\n",
    "    \"txn_hour\": np.random.randint(6, 23, M),\n",
    "    \"is_new_device\": np.random.choice([0, 1], M, p=[0.9, 0.1]),\n",
    "    \"txn_amount_inr\": np.random.choice([199, 499, 999, 1999, 3999], M,\n",
    "                                        p=[0.30, 0.28, 0.22, 0.13, 0.07]),\n",
    "    \"channel\": np.random.choice([\"P2P\", \"P2M\"], M, p=[0.4, 0.6]),\n",
    "})\n",
    "\n",
    "# inject 15 deliberate anomalies: new device, unusual hour (1-4am), high amount\n",
    "anomalies = pd.DataFrame({\n",
    "    \"txn_id\": [f\"BTXNA{i}\" for i in range(15)],\n",
    "    \"applicant_id\": np.random.choice(df[\"applicant_id\"], 15),\n",
    "    \"txn_hour\": np.random.randint(1, 5, 15),\n",
    "    \"is_new_device\": 1,\n",
    "    \"txn_amount_inr\": np.random.choice([14999, 19999, 24999], 15),\n",
    "    \"channel\": \"P2P\",\n",
    "})\n",
    "behaviour = pd.concat([behaviour, anomalies], ignore_index=True)  # 265 rows total\n",
    "behaviour.to_csv(\"txn_behaviour.csv\", index=False)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
