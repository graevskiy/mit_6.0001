#! python3

import sys

if len(sys.argv) != 4:
    sys.exit('parameters to provide annual_salary portion_saved total_cost')

try:
    annual_salary = int(sys.argv[1])
    portion_saved = float(sys.argv[2])
    total_cost = int(sys.argv[3])
except:
    sys.exit('one of your parameters is of incorrect types')

assert portion_saved < 1, 'portion_saved must be <1'

portion_down_payment = 0.25
current_savings = 0
r = 0.04

down_payment = portion_down_payment * total_cost
monthly_salary = annual_salary / 12
monthly_savings = monthly_salary * portion_saved

savings = 0
i = 0
while savings < down_payment:
    savings = monthly_savings + savings*(1+r/12)
    i += 1

print(f'You\'ll need {i} months')
