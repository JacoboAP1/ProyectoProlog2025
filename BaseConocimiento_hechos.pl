% Gran variedad de hechos para mejorar el sistema de recomendación
% destino(Nombre, Costo, Tipo, Idioma, Cultura).
destino(paris, 2000, museo, frances, europea).
destino(cancun, 1000, playa, espanol, latina).
destino(tokyo, 2500, cultura, japones, asiatica).
destino(barcelona, 1500, playa, espanol, europea).
destino(atenas, 1800, historia, griego, europea).
destino(londres, 1000, museo, ingles, europea).
destino(bariloche, 1000, playa, espanol, latina).
destino(nueva_york, 2200, ciudad, ingles, americana).
destino(roma, 1900, historia, italiano, europea).
destino(sidney, 2700, playa, ingles, oceanica).
destino(bali, 1700, playa, indonesio, asiatica).
destino(kioto, 2400, cultura, japones, asiatica).
destino(berlin, 2100, museo, aleman, europea).
destino(dubai, 2600, ciudad, arabe, arabe).
destino(el_cairo, 1600, historia, arabe, africana).
destino(machu_picchu, 1800, cultura, espanol, latina).
destino(rio_de_janeiro, 1400, playa, portugues, latina).
destino(la_habana, 1200, historia, espanol, latina).
destino(estambul, 2000, cultura, turco, euroasiatica).
destino(venecia, 2000, museo, italiano, europea).
destino(oslo, 2300, naturaleza, noruego, europea).
destino(cape_town, 1900, naturaleza, ingles, africana).
destino(vancouver, 2100, ciudad, ingles, americana).
destino(singapur, 2500, ciudad, ingles, asiatica).
destino(krakovia, 1500, historia, polaco, europea).
destino(amsterdam, 2200, museo, holandes, europea).
destino(bangkok, 1600, cultura, tailandes, asiatica).
destino(madrid, 1700, museo, espanol, europea).
destino(moscu, 2300, historia, ruso, europea).
destino(mumbai, 1500, ciudad, hindi, asiatica).
destino(helsinki, 2000, naturaleza, finlandes, europea).
destino(auckland, 2800, naturaleza, ingles, oceanica).
destino(san_francisco, 2400, ciudad, ingles, americana).
destino(lima, 1300, historia, espanol, latina).
destino(hanoi, 1700, cultura, vietnamita, asiatica).
destino(edinburgo, 1800, museo, ingles, europea).
destino(praga, 1900, historia, checo, europea).
destino(varsovia, 1400, historia, polaco, europea).
destino(buenos_aires, 1600, cultura, espanol, latina).

% Recomendación con explicación mejorada
% 1. Coincide gusto, idioma, cultura, presupuesto
recomendar_destino(Presupuesto, Gusto, Idioma, Cultura, Destino, Explicacion) :-
    destino(Destino, Costo, Gusto, Idioma, Cultura),
    Costo =< Presupuesto,
    format(atom(Explicacion),
        'Coincide con tu gusto por ~w, tu idioma (~w), afinidad cultural (~w) y presupuesto.',
        [Gusto, Idioma, Cultura]).

% 2. Coincide gusto, idioma, presupuesto
recomendar_destino(Presupuesto, Gusto, Idioma, _Cultura, Destino, Explicacion) :-
    destino(Destino, Costo, Gusto, Idioma, _),
    Costo =< Presupuesto,
    format(atom(Explicacion),
        'Coincide con tu gusto por ~w, tu idioma (~w) y presupuesto.',
        [Gusto, Idioma]).

% 3. Coincide gusto, cultura, presupuesto
recomendar_destino(Presupuesto, Gusto, _Idioma, Cultura, Destino, Explicacion) :-
    destino(Destino, Costo, Gusto, _, Cultura),
    Costo =< Presupuesto,
    format(atom(Explicacion),
        'Coincide con tu gusto por ~w, afinidad cultural (~w) y presupuesto.',
        [Gusto, Cultura]).
