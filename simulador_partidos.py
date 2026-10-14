"""
Simulador de partidos de tenis, bádminton y ping-pong.

El jugador A gana cada punto con probabilidad p (el jugador B, con 1 - p).
Se simulan partidos y se cuentan los partidos que gana A, 
obteniendo su probabilidad de victoria.
"""

import random  # Para generar números aleatorios.

import matplotlib.pyplot as plt  # Para dibujar los gráficos.

# Resultados posibles de un partido (sets de A - sets de B)
MARCADORES = {
    'tenis': ['3-0', '3-1', '3-2', '2-3', '1-3', '0-3'],
    'badminton': ['2-0', '2-1', '1-2', '0-2'],
    'pingpong': ['3-0', '3-1', '3-2', '2-3', '1-3', '0-3']
}

# ----------------------------------------------------------------------
# TENIS
def jugar_game(p, p_presion) -> bool:
    """Juega un game de tenis. Devuelve True si lo gana A, False si lo gana B.

    Se gana al llegar a 4 puntos con 2 de diferencia.
    Cuando los dos tienen 3 puntos o más (deuce / ventaja) hay presión
    y A gana el punto con probabilidad 'p_presion' en lugar de p."""
    puntos_a = 0
    puntos_b = 0

    while True:
        # Si se está en deuce/ventaja
        if puntos_a >= 3 and puntos_b >= 3:
            prob = p_presion
        else:
            prob = p

        # Se juega un punto: random.random() da un número entre 0 y 1.
        # Si es menor que prob, el punto es para A.
        if random.random() < prob:
            puntos_a += 1
        else:
            puntos_b += 1

        # Se comprueba si el juego se ha terminado.
        if puntos_a >= 4 and puntos_a - puntos_b >= 2:
            return True
        if puntos_b >= 4 and puntos_b - puntos_a >= 2:
            return False

def jugar_tiebreak(p_presion) -> bool:
    """Juega un tie-break. Se gana al llegar a 7 puntos con 2 de diferencia.
    Devuelve True si lo gana A, False si lo gana B.
    Todos sus puntos son de presión."""
    puntos_a = 0
    puntos_b = 0

    while True:
        if random.random() < p_presion:
            puntos_a += 1
        else:
            puntos_b += 1

        if puntos_a >= 7 and puntos_a - puntos_b >= 2:
            return True
        if puntos_b >= 7 and puntos_b - puntos_a >= 2:
            return False

def jugar_set_tenis(p, p_presion) -> bool:
    """Juega un set de tenis. Se gana al llegar a 6 games con 2 de diferencia.
    Si se llega a 6-6, se juega un tie-break que decide el set."""
    games_a = 0
    games_b = 0

    while True:
        if jugar_game(p, p_presion): # Si A gana el juego.
            games_a += 1
        else: # Si A pierde el juego.
            games_b += 1

        if games_a >= 6 and games_a - games_b >= 2: # A gana mínimo 6 juegos con diferencia de 2.
            return True
        if games_b >= 6 and games_b - games_a >= 2:
            return False
        if games_a == 6 and games_b == 6: # Si van 6-6 se juega tie-break.
            return jugar_tiebreak(p_presion)

# ----------------------------------------------------------------------
# BÁDMINTON Y PING-PONG
def jugar_set_raqueta(p, puntos_objetivo, tope) -> bool:
    """Juega un set de bádminton o ping-pong.

    Se gana al llegar a 'puntos_objetivo' con 2 de diferencia.
    Si hay 'tope' (bádminton: 30), quien llegue a ese número gana."""
    puntos_a = 0
    puntos_b = 0

    while True:
        if random.random() < p:
            puntos_a += 1
        else:
            puntos_b += 1

        if puntos_a >= puntos_objetivo and puntos_a - puntos_b >= 2:
            return True
        if puntos_b >= puntos_objetivo and puntos_b - puntos_a >= 2:
            return False
        if puntos_a == tope:
            return True
        if puntos_b == tope:
            return False

# ----------------------------------------------------------------------
# JUGAR UN PARTIDO COMPLETO
def jugar_partido(deporte, p, p_presion) -> bool:
    """Juega un partido completo. Devuelve True si lo gana A."""
    # Reglas del deporte.
    if deporte == 'tenis':
        sets_para_ganar = 3       # Mejor de 5 sets.
    elif deporte == 'badminton':
        sets_para_ganar = 2       # Mejor de 3 sets.
    elif deporte == 'pingpong':
        sets_para_ganar = 3       # Mejor de 5 sets.

    sets_a = 0
    sets_b = 0

    while sets_a < sets_para_ganar and sets_b < sets_para_ganar:
        # Se juega un set.
        if deporte == 'tenis':
            gana_a = jugar_set_tenis(p, p_presion)
        elif deporte == 'badminton':
            gana_a = jugar_set_raqueta(p, puntos_objetivo=21, tope=30)
        else:  # Ping-pong (no tiene tope de puntos).
            gana_a = jugar_set_raqueta(p, puntos_objetivo=11, tope=None)

        if gana_a:
            sets_a += 1
        else:
            sets_b += 1

    return sets_a, sets_b

def simular(deporte, p, p_presion=None, n_partidos=10000):
    """Se simulan n_partidos y devuelve la fracción que gana A (entre 0 y 1).
    'prob_ganar_partido': fracción de partidos que gana A (entre 0 y 1)
    'marcadores':         fracción de partidos que acaban en cada marcador
                              (por ejemplo {"3-0": 0.21, "3-1": 0.25, ...})"""
    if p_presion is None:
        p_presion = p # Sin presión: todos los puntos son igual de importantes.

    victorias = 0
    veces_resultado = {marcador: 0 for marcador in MARCADORES[deporte]}

    for _ in range(n_partidos):
        sets_a, sets_b = jugar_partido(deporte, p, p_presion)
        veces_resultado[f'{sets_a}-{sets_b}'] += 1
        if sets_a > sets_b:
            victorias += 1
 
    marcadores = {}
    for marcador, cantidad in veces_resultado.items():
        marcadores[marcador] = cantidad / n_partidos
 
    return {'prob_ganar_partido': victorias / n_partidos, 'marcadores': marcadores}

# ----------------------------------------------------------------------
# PROGRAMA PRINCIPAL: tabla y gráfica
if __name__ == "__main__":
    random.seed(42)    # Semilla: así los resultados se pueden repetir.

    # Ejemplo: marcadores finales de cada deporte cuando p = 0.52
    for deporte in ['tenis', 'badminton', 'pingpong']:
        resultado = simular(deporte, 0.52)
        print(f"\n{deporte} con p = 0.52  (gana el partido: {resultado['prob_ganar_partido']:.3f})")
        for marcador, fraccion in resultado['marcadores'].items():
            print(f'    {marcador}: {fraccion * 100:.1f} %')
    print()

    # Valores de p: 0.40, 0.41, ... , 0.60
    valores_p = [0.40 + 0.01 * i for i in range(21)]

    plt.figure(figsize=(8, 5))

    for deporte in ['tenis', 'badminton', 'pingpong']:
        resultados = []
        for p in valores_p:
            resultados.append(simular(deporte, p)["prob_ganar_partido"])
            print(f'{deporte:9s} p={p:.2f}  victorias={resultados[-1]:.3f}')
        plt.plot(valores_p, resultados, marker='o', label=deporte)

    # Línea de referencia: si el partido fuese un solo punto.
    plt.plot(valores_p, valores_p, 'k--', label='un solo punto')

    plt.xlabel('Probabilidad de ganar un punto (p)')
    plt.ylabel('Probabilidad de ganar el partido')
    plt.title('Victorias vs. p')
    plt.legend()
    plt.grid(True)
    plt.savefig('victorias_vs_p.png', dpi=150)
    plt.show()