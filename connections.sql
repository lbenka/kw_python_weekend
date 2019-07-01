SELECT 
 step1.source,
 step1.destination as transfer, 
 step2.destination,
 step1.departure_datetime,
 step1.arrival_datetime as tranfer_time,
 step2.arrival_datetime,
 step1.price,
 step1.currency,
 step2.price,
 step2.currency,
 step1.carrier,
 step2.carrier
FROM "journeys" as step1
inner join "journeys" as step2 
on step2.source=step1.destination 
where step1.arrival_datetime + interval '1 hour' < step2.departure_datetime 
and step1.carrier != step2.carrier