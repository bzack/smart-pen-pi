create table if not exists measurements (
    id varchar(64), time_utc integer, event_type varchar2, lat real, lng real, temp real, light integer 
  );
create table if not exists info (
    id varchar(64), key varchar(64), val varchar(128)
    );
