PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Users(
StudentNum char(13) primary key not null,
password text not null,
email text not null);
CREATE TABLE Record(
TicketNum char(18) primary key not null,
Item text not null,
StudentNum char(13) not null,
BroNum char(13) not null,
BeginTime TEXT NOT NULL,
Taddress TEXT    NOT NULL);
COMMIT;
