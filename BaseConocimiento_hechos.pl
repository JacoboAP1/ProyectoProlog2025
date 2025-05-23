% Solo reglas para recomendar destinos turísticos,
% sin hechos fijos, para cargar desde la base de datos.

% Regla 1:
% Coincide gusto, idioma, cultura y presupuesto
recomendar_destino(Presupuesto, Gusto, Idioma, Cultura, Destino, Explicacion) :-
    destino(Destino, Costo, Gusto, Idioma, Cultura),
    Costo =< Presupuesto,
    format(atom(Explicacion),
        'Coincide con tu gusto por ~w, tu idioma (~w), afinidad cultural (~w) y presupuesto.',
        [Gusto, Idioma, Cultura]).

% Regla 2:
% Coincide gusto, idioma y presupuesto
recomendar_destino(Presupuesto, Gusto, Idioma, _Cultura, Destino, Explicacion) :-
    destino(Destino, Costo, Gusto, Idioma, _),
    Costo =< Presupuesto,
    format(atom(Explicacion),
        'Coincide con tu gusto por ~w, tu idioma (~w) y presupuesto.',
        [Gusto, Idioma]).

% Regla 3:
% Coincide gusto, cultura y presupuesto
recomendar_destino(Presupuesto, Gusto, _Idioma, Cultura, Destino, Explicacion) :-
    destino(Destino, Costo, Gusto, _, Cultura),
    Costo =< Presupuesto,
    format(atom(Explicacion),
        'Coincide con tu gusto por ~w, afinidad cultural (~w) y presupuesto.',
        [Gusto, Cultura]).

% Regla 4:
% Coincide gusto y presupuesto
recomendar_destino(Presupuesto, Gusto, _Idioma, _Cultura, Destino, Explicacion) :-
    destino(Destino, Costo, Gusto, _, _),
    Costo =< Presupuesto,
    format(atom(Explicacion),
        'Coincide con tu gusto por ~w y presupuesto.',
        [Gusto]).

% Regla 5:
% Coincide presupuesto solamente (último recurso)
recomendar_destino(Presupuesto, _Gusto, _Idioma, _Cultura, Destino, Explicacion) :-
    destino(Destino, Costo, _, _, _),
    Costo =< Presupuesto,
    format(atom(Explicacion),
        'Coincide solo con tu presupuesto.',
        []).
