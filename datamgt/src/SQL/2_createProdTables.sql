use myasx;

create table if not exists stockProd (
    datestamp date,
    open float,
    high float,
    low float,
    close float,
    adjclose float,
    volume float,
    symbol varchar(256)
);
create table if not exists companyProd (
    name varchar(256),
    symbol varchar(256),
    GICSgroup varchar(256)
);

create table if not exists indiciesProd (
    datestamp date,
    open float,
    high float,
    low float,
    close float,
    adjclose float,
    volume float,
    symbol varchar(256)
);

alter table stockProd add constraint symbol_day unique(symbol,datestamp);
insert ignore into stockProd(select * from stockStaging); 
delete from stockProd where datestamp='0000-00-00';

alter table companyProd add constraint symbol_name unique(symbol,name);
insert ignore into companyProd(select * from companyStaging);

alter table indiciesProd add constraint symbol_day unique(symbol,datestamp);
insert ignore into indiciesProd(select * from indiciesStaging);