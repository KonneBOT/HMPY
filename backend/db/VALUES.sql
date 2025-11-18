USE zugfahrten;
INSERT INTO bahnhof (name, ort) VALUES ('Albstadt-Ebingen', 'Albstadt');
INSERT INTO bahnhof (name, ort) VALUES ('Tübingen', 'Tübingen');

-- Trains
INSERT INTO zug (name,typ,comment) VALUES ('RE 6', 'RE 3852', 'BR 612, geht voll ab in Schräglage');

SELECT * FROM bugusers;

SELECT * FROM zugfahrt;