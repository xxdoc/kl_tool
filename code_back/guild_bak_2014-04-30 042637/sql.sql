update abbendis set account_id=id where numCollected=0 and pet_crc32<>0 and account_id<>id
select *,count(id) as count from abbendis where numCollected=0 and pet_crc32<>0 and account_id<>id group by account_id limit 20

update arthas set account_id=id where numCollected=0 and pet_crc32<>0 and account_id<>id

select *,count(id) as count from arthas where numCollected=0 and pet_crc32<>0 and account_id<>id group by account_id limit 20

update aggramar set account_id=id where numCollected=0 and pet_crc32<>0 and account_id<>id
select *,count(id) as count from aggramar where numCollected=0 and pet_crc32<>0 and account_id<>id group by account_id limit 20

update argus set account_id=id where numCollected=0 and pet_crc32<>0 and account_id<>id
select *,count(id) as count from argus where numCollected=0 and pet_crc32<>0 and account_id<>id group by account_id limit 20


-802316575


update shadow_council set account_id=id where numCollected=0 and pet_crc32<>0 and account_id<>id
select *,count(id) as count from shadow_council where numCollected=0 and pet_crc32<>0 and account_id<>id group by account_id limit 20



select id,name,achievementPoints,count(id) as count from abbendis where pet_crc32>0 group by pet_crc32 having count>1 order by count desc limit 20


select a.id, a.name, a.class, a.race, a.gender, a.level, a.rank, a.guild_id, a.achievementPoints, a.pet_crc32, a.numCollected, a.lastModified, a.account_id, count(a.id) as count from wow_item_db.abbendis as a WHERE a.account_id=552  ORDER BY a.name asc LIMIT 40 OFFSET 0



select * from (select account_id as a_id,min(id) as m_id,numCollected as m_n,achievementPoints as m_a,count(id) as count from wow_item_db.abbendis WHERE numCollected>0 group by account_id,numCollected,achievementPoints having count>0 order by count desc limit 20) as m




select * from (select account_id as a_id,min(id) as m_id,numCollected as m_n,achievementPoints as m_a,count(id) as m_cc,count(distinct account_id) as m_da from wow_item_db.abbendis WHERE numCollected>0 group by numCollected,achievementPoints having m_cc>0 and m_da>1 order by m_da desc limit 20) as m



select account_id as a_id,min(id) as m_id,numCollected as m_n,achievementPoints as m_a,count(id) as m_cc,pet_crc32 as pc from wow_item_db.abbendis WHERE numCollected=34 and achievementPoints= 5985 group by account_id



select id,name,achievementPoints,guild_id,numCollected,lastModified,account_id from abbendis where account_id=552



update abbendis set account_id=min(id) where pet_crc32= and pet_crc32>0 and numCollected>0 group by pet_crc32 having ci>1



select min(id) as mi,pet_crc32 as  pc,count(id) as ci from abbendis where pet_crc32>0 and numCollected>0 group by pet_crc32 having ci>1 order by ci desc



DROP TABLE  IF EXISTS aaa_del_id_tmp

CREATE TABLE aaa_del_id_tmp (select min(id) as mi,pet_crc32 as  pc,count(id) as ci from abbendis where pet_crc32>0 and numCollected>0 group by pet_crc32 having ci>1 order by ci desc)



update abbendis as t,aaa_del_id_tmp as a set t.account_id=a.mi where t.pet_crc32=a.pc




select count(*) as count from abbendis where id in (selelct max(rowid) from abbendis group by id,a)



select count(id) from xxx where id in (select max(id) from xxx group by account_id)





DROP TABLE  IF EXISTS aaa_del_id_tmp

CREATE TABLE aaa_del_id_tmp (select min(id) as id,pet_crc32,count(id) as m_cc,count(distinct account_id) as m_da from abbendis WHERE numCollected>0 and pet_crc32<>0 group by pet_crc32 having m_cc>0 and m_da>1 order by m_da desc )

update abbendis as t inner join aaa_del_id_tmp as a using(id) set t.account_id=a.id where t.pet_crc32=a.pet_crc32 and t.account_id<>a.id




DROP TABLE  IF EXISTS aaa_del_id_tmp


update abbendis set numCollected=-999 where name in (select name from abbendis group by name having count(name)>1) and id not in (select max(id) from  abbendis  group by name  having count(name)>1)


select id from abbendis where name in (select name from abbendis group by name having count(name)>1) and id not in (select max(id) from  abbendis  group by name  having count(name)>1)


select max(id) as id,name,count(name) as cn from abbendis group by name having cn>1 order by cn desc limit 20


select max(id) from  abbendis  group by name  having count(name)>1


