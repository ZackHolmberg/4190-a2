from objects.factor import Factor
from functions import inference, sumout, multiply, observe, normalize


print('======GIVEN FACTORS======')


trav = Factor('TRAV')
trav.init([0.95, 0.05])
print(trav)

own_computer = Factor('OC')
own_computer.init([0.3, 0.7])
print(own_computer)

fraud = Factor('FRAUD|TRAV')
fraud.init([0.996, 0.004, 0.99, 0.01])
print(fraud)

computer_purchase = Factor('CRP|OC')
computer_purchase.init([0.999, 0.001, 0.9, 0.1])
print(computer_purchase)

internet_purchase = Factor('IP|FRAUD,OC')
internet_purchase.init([0.999, 0.001, 0.99, 0.01, 0.989, 0.011, 0.98, 0.02])
print(internet_purchase)

foreign_purchase = Factor('FP|FRAUD,TRAV')
foreign_purchase.init([0.99, 0.01, 0.1, 0.9, 0.9, 0.1, 0.1, 0.9])
print(foreign_purchase)


print('======INFERENCE CALCULATION FOR Q2B1======')


factor_list = [trav, own_computer, fraud, computer_purchase, internet_purchase, foreign_purchase]
query_variables = ['FRAUD']
ordered_hidden_variables = ['TRAV', 'FP', 'FRAUD', 'IP', 'OC', 'CRP']
evidence_list = []

inferenced = inference(factor_list, query_variables, ordered_hidden_variables, evidence_list)
print('>: Inference result')
print(inferenced)


print('======INFERENCE CALCULATION FOR Q2B2======')


factor_list = [trav, own_computer, fraud, computer_purchase, internet_purchase, foreign_purchase]
query_variables = ['FRAUD']
ordered_hidden_variables = ['TRAV', 'FP', 'FRAUD', 'IP', 'OC', 'CRP']
evidence_list = ['+fp', '-ip', '+crp']

inferenced = inference(factor_list, query_variables, ordered_hidden_variables, evidence_list)
print('>: Inference result')
print(inferenced)
