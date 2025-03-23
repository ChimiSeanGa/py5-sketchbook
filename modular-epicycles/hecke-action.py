from sage.all import *

f = EllipticCurve('11.a1').newform()
print(f.q_expansion(100).list())

p = 13
g = hecke_operator_on_qexp(f.q_expansion(100*p), Integer(p), Integer(2), prec=100)
print(g.list())