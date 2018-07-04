import numpy as np
import pandas as pd

time_horizon = 26

r_return = 0.0993
lump_sum = 2000
monthly = 200

investment = np.fv(rate=r_return/12, nper=time_horizon*12, pmt=monthly, pv=lump_sum, when='end')
print("Investment will yield a total of R" + str(round(-investment, 2)) + " in " + str(time_horizon) + " years")

time_horizons = np.array([i for i in range(1, 51)])
return_rates = np.array([0.0721, 0.0993, 0.1218, 0.1659, 0.18])
lump_sums = np.array([0, 350, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 10000, 15000, 20000, 25000, 30000])
monthly_contribs = np.array([0, 100, 200, 300, 500, 700, 1000, 1500, 2000, 2500])

# will be used by pandas apply() in order to determine if each investment combo is valid. 
def is_valid_investment_params(row):
    time_horizon = row["Time_Horizon"]
    lump_sum = row["Lump_Sum"]
    monthly_contrib = row["Monthly_Contrib"]
    
    periods = time_horizon * 12
    
    ##### dealing with the easy cases first ####

    # not allowed to contribute more than R33,000 per year, so lump sum cannot be greater than this amount.
    if lump_sum > 33000:
        return False
    
    # total lifetime contributions cannot be greater than R500,000, so let's check that.
    if (lump_sum + periods*monthly_contrib) > 500000:
        return False

    ##### Now the more challenging part, ensuring the contribution in any given month doesn't exceed R33,000 per year or R500,000 in total. #####

    # if the contributions in a single year + the lump sum exceed 33,000, reject the investment option.
    total = lump_sum
    for i in range(1, 13):
        total = total + monthly_contrib
        if total > 33000:
            return False
    return True
    
    #num_periods = 0   

investment_options = np.stack(np.meshgrid(time_horizons, return_rates, lump_sums, monthly_contribs), -1).reshape(-1, 4)

df = pd.DataFrame(investment_options, columns=["Time_Horizon", "Return_Rate", "Lump_Sum", "Monthly_Contrib"], dtype='float64')
df["Valid_Investment"] = df.apply(is_valid_investment_params, axis=1)
df.to_csv('taxfree_investment_options.csv', index=False)   


#investments = np.fv(rate=return_rates/12, nper=time_horizons*12, pmt=monthly_contribs, pv=lump_sums, when='end')
investments = np.round(np.fv(rate=return_rates/12, nper=time_horizon*12, pmt=monthly, pv=lump_sum, when='end') ,2)
print(-investments)