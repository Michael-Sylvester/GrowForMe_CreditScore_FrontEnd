import requests
import io
import pandas as pd

csv_content = """farmer_id,farmer_name,gender,region,drought_flood_index,savings_ghs,payment_frequency,farmer_budget_ghs,crop_types,is_association_member,has_motorbike,acres,satellite_verified,repayment_rate,yield_data,endorsements,irrigation_type,irrigation_scheme,market_access_index,training_sessions,livestock_value_ghs,alternative_income_ghs,insurance_type,insurance_subscription,digital_score,soil_health_index
1001,John Doe,male,Ashanti,20,8000,10,20000,staple,True,True,3.5,True,80,"100,110",2,canal,True,50,3,1000,500,crop,True,60,50
"""

response = requests.post(
    'https://grow4me.onrender.com/score/batch/rule-based/csv',
    files={'file': ('test.csv', io.BytesIO(csv_content.encode()), 'text/csv')}
)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
