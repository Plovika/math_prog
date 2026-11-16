from fractions import Fraction as F
from itertools import combinations, product, permutations
from math import comb, log, sqrt, pi, acos
from scipy.integrate import quad
import sys
sys.path.insert(0,str(__import__('pathlib').Path(__file__).parent))
from build_notebooks import TASKS

# Exact enumeration of all gender patterns, independent of the simulator.
patterns=list(combinations(range(10),5))
female_ok=sum(all(b-a>1 for a,b in zip(x,x[1:])) for x in patterns)
male_block=sum(max(set(range(10))-set(x))-min(set(range(10))-set(x))==4 for x in patterns)
assert F(female_ok,len(patterns))==F(male_block,len(patterns))==F(1,42)

# Exhaustive stopping words give an independent check on the coin law.
for p in [F(1,2),F(7,10)]:
    for k in range(2,10):
        probability=F(0)
        for bits in product([0,1],repeat=k):
            if bits[-1]!=bits[-2]:continue
            if any(bits[i]==bits[i+1] for i in range(k-2)):continue
            h=sum(bits)
            probability+=p**h*(1-p)**(k-h)
        m=k//2;r=p*(1-p)
        formula=(p*p+(1-p)**2)*r**(m-1) if k%2==0 else r**m
        assert probability==formula

# Integrate piecewise products of minima exactly, separate from J/K formulae.
def integral_formula(w):
    total=F(0)
    for j in range(len(w)):
        others=w[:j]+w[j+1:]
        cuts=sorted(set([F(0),F(1)]+others))
        for lo,hi in zip(cuts,cuts[1:]):
            midpoint=(lo+hi)/2
            constant=F(1);degree=0
            for value in others:
                if midpoint<value:degree+=1
                else:constant*=value
            total+=constant*(hi**(degree+1)-lo**(degree+1))/(degree+1)
    return total

# Load only the probability definition, not the Monte Carlo code.
scope={'Fraction':F}
exec(TASKS[11]['code'].split('N = 150_000')[0],scope)
for n in [2,3,4]:
    for w in combinations([F(0),F(1,5),F(1,3),F(1,2),F(1)],n):
        actual=scope['probability'](w)
        assert actual==integral_formula(list(w))
        assert scope['probability'](w[::-1])==actual
    for q in [F(0),F(1,4),F(1)]:
        assert scope['probability']([q]*n)==n*q**(n-1)-(n-1)*q**n
assert scope['probability']([F(1,4),F(1,3),F(1,2)])==F(1435,5184)
assert scope['probability']([F(1,5),F(1,4),F(1,2)])==F(9947,48000)

# Independent quadrature checks the longer analytic integrations.
broken=6*(quad(lambda t:3*t-1,F(1,3),.5)[0]-quad(lambda t:sqrt((t+1)**2-2),sqrt(2)-1,.5)[0])
assert abs(broken-(3*log(2)-2))<1e-9
disk=quad(lambda d:(4*d*acos(d/2)-d*d*sqrt(4-d*d))/pi,0,1)[0]
assert abs(disk-(1-3*sqrt(3)/(4*pi)))<1e-10
L,H,r=40,16,11
rectangle=quad(lambda u:2*(L-u)/L**2*(2*sqrt(r*r-u*u)/H-(r*r-u*u)/H**2),0,r)[0]
closed=(pi*L*H*r*r-4*(L+H)*r**3/3+r**4/2)/(L*L*H*H)
assert abs(rectangle-closed)<1e-10
print('Exact enumeration, stopping laws, waiting formulae, boundary cases and integrals: PASS')
