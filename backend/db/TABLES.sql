USE zugfahrten;

# create table mit namen bugusers
create table IF NOT EXISTS bugusers(id int not null auto_increment, primary key(id));
alter table bugusers add column username varchar(30) not null;
alter table bugusers add column email_address varchar(50) not null;
alter table bugusers add column password varchar(60) not null;


# make entrfries unique, see ticketusers above
ALTER TABLE bugusers ADD UNIQUE (username);
ALTER TABLE bugusers ADD UNIQUE (email_address);

-- Tabelle: zug
CREATE TABLE zug (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    typ VARCHAR(100),
    comment VARCHAR(512)
);

-- Tabelle: bahnhof
CREATE TABLE bahnhof (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ort VARCHAR(255)
);

-- Tabelle: zugfahrt
CREATE TABLE IF NOT EXISTS zugfahrt (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_station_id INT NOT NULL,
    end_station_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    train_id INT,
    comment VARCHAR(512),
    delay INT,

    CONSTRAINT fk_start_station FOREIGN KEY (start_station_id) REFERENCES bahnhof(id),
    CONSTRAINT fk_end_station FOREIGN KEY (end_station_id) REFERENCES bahnhof(id),
    CONSTRAINT fk_train FOREIGN KEY (train_id) REFERENCES zug(id)
);