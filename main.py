import sys, hashlib
import validator as v

def go():
    print()
    print("+" + "-"*38 + "+")
    print("|          GIT UNLOCK  v0.9.0          |")
    print("+" + "-"*38 + "+")
    r = v.validar()
    t = [x for x in r if not x[1]]
    z = len(r)
    if len(t) > 0:
        print("\n[X] PROGRAMA BLOQUEADO\n")
        print("Este programa ainda nao foi liberado.")
        print("Investigue o repositorio.\n")
        return 1
    h = v.g('rev-parse','HEAD'); k = hashlib.sha256((h+v.TAG).encode()).hexdigest()[:12].upper()
    print("\n[OK] PROGRAMA ATIVADO\n"); print("Codigo de ativacao:", k)
    print()
    return 0

if __name__ == '__main__':
    sys.exit(go())
