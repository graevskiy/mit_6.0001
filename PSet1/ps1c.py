#! python3

import sys

if len(sys.argv) != 2:
    sys.exit('parameters to provide annual_salary')

try:
    annual_salary = int(sys.argv[1])
except:
    sys.exit('one of your parameters is of incorrect types')


# need to find portion_saved

semi_annual_raise = 0.07
portion_down_payment = 0.25
current_savings = 0
r = 0.04
total_cost = 1000000

down_payment = portion_down_payment * total_cost
monthly_salary = annual_salary / 12


def calc_months(rate):
    savings = 0
    i = 0
    monthly_savings = round(monthly_salary * rate/100, 2)
    while savings < down_payment:
        if i>5 and i%6 == 1:
            monthly_savings += round(monthly_savings*semi_annual_raise, 2)        
        savings = monthly_savings + savings*(1+r/12)
        # print(monthly_savings, savings)
        i += 1

    return i, savings


def bisect_s(low_b, hi_b, j):
    j += 1
    rate = round((hi_b + low_b) / 2, 2)

    if rate == hi_b:
        return None, rate, j

    steps, savings = calc_months(rate)

    if steps < 36:
        steps, rate, j = bisect_s(low_b, rate, j)
    elif steps > 36:
        steps, rate, j = bisect_s(rate, hi_b, j)
    else:
        if savings > down_payment + 100:
            steps, rate, j = bisect_s(low_b, rate, j)
        elif savings < down_payment - 100:
            steps, rate, j = bisect_s(rate, hi_b, j)

    return steps, rate, j

j = 0
steps, rate, j = bisect_s(0, 100, j)

if steps:
    print(j, rate)
else:
    print('no solution')