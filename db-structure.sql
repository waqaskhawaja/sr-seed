drop table fact_call cascade;
drop table dim_agent cascade;
drop table dim_deal cascade;
drop table dim_call_type cascade;
drop table dim_disposition cascade;

CREATE TABLE IF NOT EXISTS dim_agent (
   id serial PRIMARY KEY,
   agent_name varchar(100),
   role_name varchar(100),
   extension smallint
);

CREATE TABLE IF NOT EXISTS dim_deal (
   id serial PRIMARY KEY,
   phone_number varchar(100)
);

CREATE TABLE IF NOT EXISTS dim_call_type (
   id serial PRIMARY KEY,
   call_type varchar(25)
);

CREATE TABLE IF NOT EXISTS dim_disposition (
   id serial PRIMARY KEY,
   disposition varchar(25)
);

CREATE TABLE IF NOT EXISTS fact_call (
   id serial PRIMARY KEY,
   unique_id varchar(50) UNIQUE,
   duration smallint,
   billable_duration smallint,
   call_timestamp timestamptz,
   dim_agent_id integer REFERENCES dim_agent (id),
   dim_deal_id integer REFERENCES dim_deal (id),
   dim_call_type_id integer REFERENCES dim_call_type (id),
   dim_disposition_id integer REFERENCES dim_disposition (id)
);

insert into dim_agent(agent_name, role_name, extension) values('Sheraz', '', 2001);
insert into dim_agent(agent_name, role_name, extension) values('Rabia','Sales', 2002);
insert into dim_agent(agent_name, role_name, extension) values('Sania','Sales', 2003);
insert into dim_agent(agent_name, role_name, extension) values('Jaweria','Sales', 2004);
insert into dim_agent(agent_name, role_name, extension) values('Ehsan','', 2005);
insert into dim_agent(agent_name, role_name, extension) values('Waqas','', 2006);
insert into dim_agent(agent_name, role_name, extension) values('Voice Mail','', 6000);

insert into dim_call_type(call_type) values('Incoming');
insert into dim_call_type(call_type) values('Outgoing');

insert into dim_disposition(disposition) values('ANSWERED');
insert into dim_disposition(disposition) values('NO ANSWER');
insert into dim_disposition(disposition) values('BUSY');
insert into dim_disposition(disposition) values('FAILED');
