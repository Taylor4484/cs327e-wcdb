use cs327e_taylor

/* -*- coding: cp1252 -*-*/
/*1. Which people are associated with more than one crisis?*/

Select first_name, middle_name, last_name
    From Person
    Where id in
  (select id_person as id
	    From PersonCrisis 
            having count(id_crisis) > 1);

/*2. For the past 5 decades, which countries had the most world crises per decade?*/

Select country
    From Location join Crisis
    on Location.entity_id = Crisis.id
    Where start_date >= 1963-01-01;
/*3. What is the average death toll of accident crises?*/

Select avg(number)
    From HumanImpact
    Where type = 'Death' AND crisis_id in
	(select id as crisis_id
	    from Crisis
	    Where kind = 'ACC');

/*4. What is the average death toll of world crises per country?*/

Select avg(number), country
	From HumanImpact as S join Location as R
	On S.crisis_id = R.id
	Where type = 'Death'
	Group by country;
	
/*5. What is the most common resource needed?*/
select * 
	 from Crisis join ResourceNeeded 
	 	 on Crisis.id = ResourceNeeded.crisis_id;

/*6. How many persons are related to crises located in countries other than their own?*/

select * 
from Person join Location
on Person.id = Location.entity_id
order by country;


/*7. How many crises occurred during the 1960s?*/

Select count(name)
	From Crisis
	Where start_date > 1959-12-31 AND start_date < 1970-01-01;

/*8. Which orgs are located outside the United States and were involved in > 1 crisis?*/

select name
from 


(Select distinct name 
	From Organization join Location
	Where Location.country !='United States' or 'US' or 'USA' or 'United States of America') as T

Natural Join

	
(select distinct  id_organization 
from CrisisOrganization
having count(id_organization) > 1) as S;

/*9. Which Orgs, Crises, and Persons have the same location (country)?*/

Select R.name, S.name, T.first_name, T.last_name, U.country
    From Organization as R join Crisis as S join Person as T join Location as U
    On S.id=U.id AND R.id=U.id AND T.id=U.id
    Where R.country = U.country
    Order by country;

/*10. Which crisis has the minimum Human Impact?*/

Select Crisis.name, min(HumanImpact.number)
    From Crisis join HumanImpact
    on Crisis.id = HumanImpact.crisis_id;

/*11. Count the number of crises that each organization is associated with?*/

Select name, count(id_crisis)
    From CrisisOrganization as S join Organization as R 
    on S.id_organization= R.id;

/*12. Name and Postal Address of all orgs in California?*/


Select name, street_address, locality, region, postal_code
    From Organization
    Where id in
	(Select entity_id as id
	    From Location
	    Where region = 'California');


/*13. List all crises that happened in the same state/region and country, list in descinding order*/

Select name, region, Location.country
    From Crisis join Location
    on Crisis.id = Location.entity_id
    group by region;

/*14. Find the total number of human casualties caused by crises in the 1990s?*/

Select count(number)
    From HumanImpact
    Where type = 'Death' and crisis_id in
	(Select id as crisis_id
	    From Crisis
	    Where start_date >= 1990-01-01 AND start_date < 2000-01-01);

/*15. Find the organization(s) that has provided support on the most Crises?*/

Select Organization.name
    From Organization join CrisisOrganization
    on Organization.id = CrisisOrganization.id_organization
    order by count(CrisisOrganization.id_crisis);
/*16. How many organizations are government based?*/

Select count(name)
	From Organization
	Where kind = 'GOV';

/*17. What is the total number of casualties across the DB?*/


Select SUM(number)
	From HumanImpact
	where type = 'Death';


/*18. What is the most common type/kind of crisis occurring in the DB?*/

Select kind, count(kind)
	From Crisis
	group by kind
	order by count(kind) desc;


/*19. Create a list of telephone numbers, emails, and other contact info for all orgs*/

Select name, telephone, fax, email, street_address, locality, region, postal_code,country
     From Organization;

/*20. What is the longest-lasting crisis? (if no end date, then ignore)*/

Select R.name, max(S.end_date - R.start_date)
     From Crisis as R join Crisis as S 
     where S.end_date != 0000-00-00 and
     R.start_date != 0000-00-00;


/*21. Which person(s) is involved or associated with the most organizations?*/

Select first_name, middle_name, last_name
	From Person;

/*22.How many hurricane crises (CrisisKind=HU)?*/

Select count(*)
     From Crisis
     Where kind = 'HU';

/*23. Name all humanitarian orgs in the DB*/

Select name
	From Organization
	Where kind = 'HO'
	Order by name desc;

/*24. List the crises in the order when they occurred (earliest to latest)*/

Select name
    From Crisis
    Order by start_date asc;

/*25. Get the name and kind of all persons in the US (United States, USA, United States of America)*/

Select first_name, middle_name, last_name, kind
     From Person join Location
     on Person.id = Location.entity_id
     Where (country = 'United States') OR (country = 'USA') OR (country = 'United States of America') or (country = 'US');

/*26. Who has the longest name?*/

Select first_name, middle_name, last_name
	From Person
	having max(length(first_name) + length(middle_name) + length(last_name));

/*27. Which kinds of crisis only have one crisis example?*/


Select C.kind
	From Crisis as C join CrisisKind as K
	On C.kind = K.id
	having count(C.kind) = 1;


/*28. Which people don't have a middle name?*/

Select first_name, middle_name, last_name
     From Person
     where middle_name = 'NULL';

/*29. What are the names that start with 'B'?*/

Select first_name, middle_name, last_name
      From Person
      Where first_name LIKE 'B%';

/*30. List all the people associated with each country.*/

Select first_name, middle_name, last_name, country
     From Person join Location
     on Person.id = Location.entity_id
     Order by country;

/*31. What crisis affected the most countries?*/
Select country, count(Crisis.id)
	From Crisis join Location
    on Crisis.id = Location.entity_id
	order by (count(Crisis.id));

/*32.What is the first (earliest) crisis in the database?*/

Select name, start_date
	From Crisis 
	order by start_date limit 1;

/*33. What is the number of organizations in the US?*/


Select count(*)
	From Organization join Location
	on Organization.id = Location.entity_id 
	Where (Location.country = 'United States') OR (Location.country = 'USA') OR (Location.country = 'United States of America') or (Location.country = 'US');

/*34.How many people are singers?*/

Select count(*)
	From Person
	Where kind = 'SNG';

/*35.What is the number of leaders (current and former)? (PersonKind is "LD")*/

Select count(*)
	From Person
	Where kind = 'LD';

/*36. Find the start date of every hurricane that occurred in the US*/

Select start_date, name
	From Crisis join Location on Crisis.id = Location.entity_id
	Where kind = 'HU' AND (country = 'United States' OR country = 'US' OR country = 'United States of America');

/*37. Number of natural disasters occurring from June 5th 2000 to June 5th 2012*/

Select count(*)
	From Crisis 
	Where kind= 'EQ' OR 'FR' OR 'FL' OR 'HU' OR 'ME' OR 'ST' OR 'TO' OR 'TS' OR 'VO' 
	and start_date > 2000-06-05 AND start_date < 2012-06-05 ;

/*38. Number of political figures grouped by country.*/

Select country, count(*) as Political_Figures
	From Person join Location
	on Person.id = Location.entity_id
	Where kind = 'DI' OR kind = 'FRC' OR kind = 'GO' OR kind = 'GOV' OR kind ='PO' OR kind ='PR' OR kind ='PM' OR kind ='SA' OR kind ='AMB' OR kind = 'VP'
        Group by country;

/*39.Location with the most number of natural disasters*/

Select Location.country, count(*) as T
	From Location join Crisis
	on Location.entity_id = Crisis.id
	Where kind = 'EQ' OR kind =  'FR' OR kind =  'FL' OR kind =  'HU' OR kind =  'ME' OR kind =  'ST' OR kind =  'TO' OR kind =  'TS' OR kind =  'VO'
	order by T;

/*40.Average number of deaths caused by hurricanes.*/

Select avg(number)
	From HumanImpact join Crisis
	On HumanImpact.crisis_id = Crisis.id
	Where kind = 'HU' AND type = 'Death';

/*41. Total number of deaths caused by terrorist attacks*/

Select sum(number)
	From HumanImpact join Crisis
	On HumanImpact.crisis_id = Crisis.id
	Where kind = 'TA' and number IS NOT NULL;

/*42. List of Hurricanes in the US that Wallace Stickney (WStickney) helped out with.*/

Select name
	From Crisis
	Where kind= 'HU' AND id in 
		(select id_crisis as id
			From PersonCrisis
			Where id_person = 'WStickney');

/*43.List of hurricanes in the US where FEMA was NOT involved.*/

Select distinct name
	From Crisis join CrisisOrganization
	on Crisis.id = CrisisOrganization.id_Crisis
	Where kind = 'HU' AND not id_organization = 'FEMA';


/*44.  Number of crises that intelligence agencies were involved in.*/

Select count(*)
	From CrisisOrganization join Organization
	On CrisisOrganization.id_organization = Organization.id
	Where id in
		(Select id 
			From Organization
			Where kind = 'IA');

/*45. How many more orgs does America have than Britain.*/ 

Select count(S.id) - count(R.id)
	From Organization as S join Organization as R natural join Location
	Where S.Country = 'Britain' AND R.Country = 'United States';
