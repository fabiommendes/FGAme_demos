'''
Nesta atividade vamos modificar a função de resolução de colisões da FGAme.
Modifique a função resolve_collision(col) abaixo para que ela implemente a
transferência de impulso usando as fórmulas aprendidas em sala de aula.
'''

from FGAme import *
from FGAme import patch


@patch.set_resolve_collision
def resolve_collision(col):
    '''Implementa uma rotina de resolução de colisão.
    O objeto de entrada `col` guarda várias informações importantes em seus
    atributos como o vetor normal em `col.normal`, o ponto de contato em
    `col.pos`, o coeficiente de restituição em `col.restitution` e a frição em
    `col.friction`.
    Documentação adicional sobre os objetos do tipo `Collision` pode ser
    encontrada no módulo :mod:`FGAme.physics.collision`. A rotina padrão para a
    resolução de colisões na FGAme pode ser acessada pelo método
    `col.resolve()`.
    '''

    # Este exemplo utiliza a estratégia ingênua de resolver as colisões apenas
    # invertendo as velocidades de cada objeto. Como podemos ver, isto não
    # funciona!
    #
    # Implemente aqui a rotina correta.
    A, B = col
    n = col.normal
    e = col.restitution
    Vrel = (B.vpoint(col.pos) - A.vpoint(col.pos)).dot(n)
    
    if Vrel < 0:   
        
        rA = col.pos - A.pos
        rB = col.pos - B.pos
        invm = A.invmass + B.invmass
        invm += rA.cross(n)**2 / A.inertia
        invm += rB.cross(n)**2 / B.inertia
        
        m = 1/invm
        
        J = m * (1 + e) * Vrel
        
        Jvec = J * n
        A.apply_impulse(Jvec, pos = col.pos)
        B.apply_impulse(-Jvec, pos = col.pos)


    
# Aqui chamamos uma simulação já pronta para testar nosso método de resolução
# de colisões.
from FGAme.demos.simulations import gas_polys
