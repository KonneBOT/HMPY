USE zugfahrten;

#insert into ticketusers table
INSERT INTO bugusers (id, username, email_address, password) VALUES (1, 'Derk', 'de@alb.de', 'pass');
INSERT INTO bugusers (id, username, email_address, password) VALUES (2, 'Natalie', 'na@alb.de', 'pass');
INSERT INTO bugusers (id, username, email_address, password) VALUES (3, 'Anaking', 'an@alb.de', 'pass');


# set password policy
SET GLOBAL validate_password_policy=LOW;
# create users (das )
CREATE USER 'buguser'@'%' IDENTIFIED WITH mysql_native_password BY 'Heute000';
# oben hat nicht getan:
alter user 'buguser'@'%' identified with mysql_native_password by 'Heute000';
# grant full privileges
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'buguser'@'%' WITH GRANT OPTION;
# grant partial privileges
GRANT INSERT, SELECT, DELETE, DROP, UPDATE on ticketdb.* TO 'buguser'@'%';

#show grants
show grants for 'buguser'@'%';
