from sympy import symbols, Symbol, sqrt, oo, re, nan, im, sign, I, E, log, \
        pi, arg, conjugate, expand, exp, sin, cos, Function, Abs
from sympy.utilities.pytest import XFAIL


def test_re():
    x, y = symbols('x,y')

    r = Symbol('r', real=True)

    assert re(nan) == nan

    assert re(oo) == oo
    assert re(-oo) == -oo

    assert re(0) == 0

    assert re(1) == 1
    assert re(-1) == -1

    assert re(E) == E
    assert re(-E) == -E

    assert re(x) == re(x)
    assert re(x*I) == -im(x)
    assert re(r*I) == 0
    assert re(r) == r

    assert re(x + y) == re(x + y)
    assert re(x + r) == re(x) + r

    assert re(re(x)) == re(x)

    assert re(2 + I) == 2
    assert re(x + I) == re(x)

    assert re(x + y*I) == re(x) - im(y)
    assert re(x + r*I) == re(x)

    assert re(log(2*I)) == log(2)

    assert re((2+I)**2).expand(complex=True) == 3

def test_im():
    x, y = symbols('x,y')

    r = Symbol('r', real=True)

    assert im(nan) == nan

    assert im(oo*I) == oo
    assert im(-oo*I) == -oo

    assert im(0) == 0

    assert im(1) == 0
    assert im(-1) == 0

    assert im(E*I) == E
    assert im(-E*I) == -E

    assert im(x) == im(x)
    assert im(x*I) == re(x)
    assert im(r*I) == r
    assert im(r) == 0

    assert im(x + y) == im(x + y)
    assert im(x + r) == im(x)
    assert im(x + r*I) == im(x) + r

    assert im(im(x)*I) == im(x)

    assert im(2 + I) == 1
    assert im(x + I) == im(x) + 1

    assert im(x + y*I) == im(x) + re(y)
    assert im(x + r*I) == im(x) + r

    assert im(log(2*I)) == pi/2

    assert im((2+I)**2).expand(complex=True) == 4

def test_sign():
    assert sign(1.2) == 1
    assert sign(-1.2) == -1
    assert sign(0) == 0
    x = Symbol('x')
    assert sign(x).is_zero == False
    assert sign(2*x) == sign(x)
    p = Symbol('p', positive = True)
    n = Symbol('n', negative = True)
    m = Symbol('m', negative = True)
    assert sign(2*p*x) == sign(x)
    assert sign(n*x) == -sign(x)
    assert sign(n*m*x) == sign(x)
    x = 0
    assert sign(x).is_zero == True


def test_Abs():
    x, y = symbols('x,y')
    assert Abs(0) == 0
    assert Abs(1) == 1
    assert Abs(-1)== 1
    x = Symbol('x',real=True)
    n = Symbol('n',integer=True)
    assert x**(2*n) == Abs(x)**(2*n)
    assert Abs(x).diff(x) == sign(x)
    assert abs(x) == Abs(x) # Python built-in
    assert Abs(x)**3 == x**2*Abs(x)
    assert (Abs(x)**(3*n)).args == (Abs(x), 3*n) # leave symbolic odd unchanged
    assert (1/Abs(x)).args == (Abs(x), -1)
    assert 1/Abs(x)**3 == 1/(x**2*Abs(x))

def test_abs_real():
    # test some properties of abs that only apply
    # to real numbers
    x = Symbol('x', complex=True)
    assert sqrt(x**2) != Abs(x)
    assert Abs(x**2) != x**2

    x = Symbol('x', real=True)
    assert sqrt(x**2) == Abs(x)
    assert Abs(x**2) == x**2

def test_abs_properties():
    x = Symbol('x')
    assert Abs(x).is_real == True
    assert Abs(x).is_positive == None
    assert Abs(x).is_nonnegative == True

    w = Symbol('w', complex=True, zero=False)
    assert Abs(w).is_real == True
    assert Abs(w).is_positive == True
    assert Abs(w).is_zero == False

    q = Symbol('q', positive=True)
    assert Abs(q).is_real == True
    assert Abs(q).is_positive == True
    assert Abs(q).is_zero == False

def test_arg():
    assert arg(0) == nan
    assert arg(1) == 0
    assert arg(-1) == pi
    assert arg(I) == pi/2
    assert arg(-I) == -pi/2
    assert arg(1+I) == pi/4
    assert arg(-1+I) == 3*pi/4
    assert arg(1-I) == -pi/4

    p = Symbol('p', positive=True)
    assert arg(p) == 0

    n = Symbol('n', negative=True)
    assert arg(n) == pi

def test_conjugate():
    a = Symbol('a', real=True)
    assert conjugate(a) == a
    assert conjugate(I*a) == -I*a

    x, y = symbols('x,y')
    assert conjugate(conjugate(x)) == x
    assert conjugate(x + y) == conjugate(x) + conjugate(y)
    assert conjugate(x - y) == conjugate(x) - conjugate(y)
    assert conjugate(x * y) == conjugate(x) * conjugate(y)
    assert conjugate(x / y) == conjugate(x) / conjugate(y)
    assert conjugate(-x) == -conjugate(x)

def test_issue936():
    x = Symbol('x')
    assert Abs(x).expand(trig=True)     == Abs(x)
    assert sign(x).expand(trig=True)    == sign(x)
    assert arg(x).expand(trig=True)     == arg(x)

def test_issue1655_derivative_conjugate():
    x = Symbol('x')
    f = Function('f')
    assert (f(x).conjugate()).diff(x) == (f(x).diff(x)).conjugate()

def test_derivatives_issue1658():
    x = Symbol('x')
    f = Function('f')
    assert re(f(x)).diff(x) == re(f(x).diff(x))
    assert im(f(x)).diff(x) == im(f(x).diff(x))

    x = Symbol('x', real=True)
    assert Abs(f(x)).diff(x).subs(f(x), 1+I*x).doit() == x/sqrt(1 + x**2)
    assert arg(f(x)).diff(x).subs(f(x), 1+I*x**2).doit() == 2*x/(1+x**4)
