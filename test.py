from objects.factor import Factor
from functions import sumout, multiply, observe, normalize
from objects.key_iterator import KeyIterator
from objects.relation import Relation

relation1 = Relation('A|B')
relation2 = Relation('A,B')
relation3 = Relation('A|B,C', ['-b'])
relation4 = Relation('A,B,C', ['-c'])

assert(relation1.is_conditional)
assert(relation2.is_joint)
assert(relation3.is_conditional)
assert(relation4.is_joint)

print(relation1.variables, relation1.query_variables,
      relation1.evidence_variables)
print(relation2.variables)
print(relation3.variables, relation3.query_variables,
      relation3.evidence_variables)
print(relation4.variables)
print(relation3.values)
print(relation4.values)

kit1 = KeyIterator(relation1)
kit1_rows = 0
for row in kit1:
    kit1_rows += 1
print(kit1)
assert(kit1_rows == 4)

kit2 = KeyIterator(relation2)
kit2_rows = 0
for row in kit2:
    kit2_rows += 1
print(kit2)
assert(kit2_rows == 4)


kit3 = KeyIterator(relation3)
kit3_rows = 0
for row in kit3:
    kit3_rows += 1
print(kit3)
assert(kit3_rows == 4)

kit4 = KeyIterator(relation4)
kit4_rows = 0
for row in kit4:
    kit4_rows += 1
print(kit4)
assert(kit4_rows == 4)


# Rain-traffic-late example given +r, P(+r), P(T|+r), P(L|T)
rain2 = Factor('R', ['+r'])
rain2.init([0.1])
print(rain2)

traffic2 = Factor('T|R', ['+r'])
traffic2.init([0.2, 0.8])
print(traffic2)

late2 = Factor('L|T')
late2.init([0.9, 0.1, 0.7, 0.3])
print(late2)

rt2 = multiply(rain2, traffic2)
print(rt2)

rtl2 = multiply(rt2, late2)
print(rtl2)


# R-T-L Full join and sumout:
rain3 = Factor('R')
rain3.init([0.9, 0.1])
print(rain3)

traffic3 = Factor('T|R')
traffic3.init([0.9, 0.1, 0.2, 0.8])
print(traffic3)

late3 = Factor('L|T')
late3.init([0.9, 0.1, 0.7, 0.3])
print(late3)

rt3 = multiply(rain3, traffic3)
print(rt3)

t = sumout(rt3, 'R')
print(t)

tl3 = multiply(t, late3)
l = sumout(tl3, 'T')
print(l)


# Alarm example: P(B), P(E), P(A|B,E), P(J|A), P(M|A)
burglary = Factor('B')
burglary.init([0.999, 0.001])
print(burglary)

earthquake = Factor('E')
earthquake.init([0.998, 0.002])
print(earthquake)

alarm = Factor('A|B,E')
alarm.init([0.999, 0.001, 0.71, 0.29, 0.06, 0.94, 0.05, 0.95])
print(alarm)

john = Factor('J|A')
john.init([0.95, 0.05, 0.1, 0.9])
print(john)

mary = Factor('M|A')
mary.init([0.99, 0.01, 0.3, 0.7])
print(mary)

f1 = multiply(burglary, earthquake)
f2 = multiply(f1, alarm)
f3 = multiply(f2, john)
f4 = multiply(f3, mary)
print(f4)

# ========== OBSERVE TESTS ==========
observeBefore = Factor('L|T')
observeBefore.init([0.9, 0.1, 0.7, 0.3])
print("Before observe: ", observeBefore)
observeAfter = observe(observeBefore, "T", "+")
print("After observe: ", observeAfter)

observeBefore2 = Factor('Z,T,H')
print("Before init: ", observeBefore2.relation.values)
observeBefore2.init([0.8, 0.2, 0.4, 0.6, 0.9, 0.1, 0.7, 0.3])
print("Before observe: ", observeBefore2)
observeAfter2 = observe(observeBefore2, "T", "+")
print("After observe: ", observeAfter2)

# ========== NORMALIZE TESTS ==========
normalizeBefore = Factor('Z|H')
print("Before init: ", normalizeBefore.relation.values)
normalizeBefore.init([0.8, 0.2, 0.4, 0.6])
print("Before normalization: ", normalizeBefore)
normalizeAfter = normalize(normalizeBefore)
print("After normalize: ", normalizeAfter)
assert(sum(normalizeAfter.data.values()) == 1.0)

normalizeBefore2 = Factor('Z,T,H')
print("Before init: ", normalizeBefore2.relation.values)
normalizeBefore2.init([0.8, 0.2, 0.4, 0.6, 0.9, 0.1, 0.7, 0.3])
print("Before normalization: ", normalizeBefore2)
normalizeAfter2 = normalize(normalizeBefore2)
print("After normalize: ", normalizeAfter2)
assert(sum(normalizeAfter2.data.values()) == 1.0)
