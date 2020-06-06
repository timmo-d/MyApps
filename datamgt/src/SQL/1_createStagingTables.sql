use myasx;

create table if not exists stockStaging (
    datestamp date,
    open float,
    high float,
    low float,
    close float,
    adjclose float,
    volume float,
    symbol varchar(256)
);

create table if not exists companyStaging (
    name varchar(256),
    symbol varchar(256),
    GICSgroup varchar(256)
);

create table if not exists indiciesStaging (
    datestamp date,
    open float,
    high float,
    low float,
    close float,
    adjclose float,
    volume float,
    symbol varchar(256)
);

create table if not exists updates (
    lastupdate varchar(256)
);

delete from updates;
insert into updates values ('1262304000');