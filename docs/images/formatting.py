import tellurium as te
import roadrunner

r = te.loada("""
    $X0 -> S1 ; k1*X0;
    S1 -> S2 ; k2*S1*S2^h/(10 + S2^h) + k3*S1;
    S2 -> $X3 ; k4*S2;

    h=2;
    k1 =1.0;
    k2 = 2.0;
    k3 = 0.02;
    k4 = 1.0;
    X0 = 1;
""")
