% destino(Nombre, Costo, Tipo, Idioma, Cultura).
destino(paris, 2000, museo, frances, europea).
destino(cancun, 1000, playa, espanol, latina).
destino(tokyo, 2500, cultura, japones, asiatica).
destino(barcelona, 1500, playa, espanol, europea).
destino(atenas, 1800, historia, griego, europea).
destino(londres, 1000, museo, ingles, europea).
destino(bariloche, 1000, playa, espanol, latina).

% Recomendación con explicación
recomendar_destino(Presupuesto, Gusto, Idioma, Cultura, Destino, Explicacion) :-
    destino(Destino, Costo, Gusto, IdiomaDestino, CulturaDestino),
    Costo =< Presupuesto,
    (
        IdiomaDestino = Idioma,
        format(atom(Explicacion), 'Coincide con tu gusto por ~w, tu idioma (~w) y presupuesto.', [Gusto, Idioma])
    ;
        CulturaDestino = Cultura,
        format(atom(Explicacion), 'Coincide con tu gusto por ~w, afinidad cultural (~w) y presupuesto.', [Gusto, Cultura])
    ).
