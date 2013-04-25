/* -*- coding: cp1252 -*-*/
/*1. Which people are associated with more than one crisis?*/

Select first_name, middle_name, last_name
    From Person
    Where id in
  (select id_person as id
	    From PersonCrisis 
            Where count(id) > 1);

/*2. For the past 5 decades, which countries had the most world crises per decade?*/

Select country
    From Location join Crisis
    Where id in
	(select id
	    From Crisis 
	    Where start_date >= 1963-01-01)
    Group by Country
    Order by start_date;

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

Select S.description, max(S.C)
	From (Select description, count(*) as C from Crisis as S join ResourceNeeded where S.id = R.crisis_id group by id);

/*6. How many persons are related to crises located in countries other than their own?*/

Select count(distinct ids)
	From Person join Location as R Join Location as S join PersonCrisis join Crisis
	on Person.id = R.id = PersonCrisis.id_person AND crisis.id = S.id
	where R.country != S.country;


/*7. How many crises occurred during the 1960s?*/

Select count(name)
	From Crisis
	Where start_date > 1959-12-31 AND start_date < 1970-01-01;

/*8. Which orgs are located outside the United States and were involved in > 1 crisis?*/

Select name 
	From Organization join Location
	Where County != United States or US or USA or The United States AND id in
            (select id_organization as id 
                from CrisisOrganization
                Where count(id_organization)> 1);

/*9. Which Orgs, Crises, and Persons have the same location (country)?*/

Select R.name, S.name, T.person, Country
    From Organization as R join Crisis as S join Person as T join Location as U
    On S.id=U.id AND R.id=U.id AND T.id=U.id
    Order by Country;

/*10. Which crisis has the minimum Human Impact?*/

Select name
    From Crisis 
    Where id in
        (Select crisis_id as id
	    From HumanImpact
	    Where number < ALL);

/*11. Count the number of crises that each organization is associated with?*/

Select name, count(distinct  id_crisis)
    From CrisisOrganization as S join Organization as R 
    on S.id_organization= R.id;

/*12. Name and Postal Address of all orgs in California?*/

Select name, street address, locality, region, postal_code
    From Organization
    Where id in
	(Select id
	    From Location
	    Where region = 'California');

/*13. List all crises that happened in the same state/region and country, list in descinding order*/

Select name, region
    From Crisis natural join Location
    Order by region;

/*Holly's update (haven't checked validity):
    select name from Crisis, Location
        where Location.id in (
            select id from Location as L1, Location as L2
                where L1.coutry = L2.country AND L1.region = L2.region)
        group by Location.region;
*/

/*14. Find the total number of human casualties caused by crises in the 1990s?*/

Select count(number)
    From HumanImpact
    Where crisis_id in
	(Select id as crisis_id
	    From Crisis
	    Where start_date >= 1990-01-01 AND start_date < 2000-01-01);

/*15. Find the organization(s) that has provided support on the most Crises?*/

Select name 
    From Organization
    Where id in
	(Select id_organization as id
	    From CrisisOrganization
	    Where count(id_organization) > ALL);

/*16. How many organizations are government based?*/

Select count(name)
	From Organizations
	Where kind = 'GOV';

/*17. What is the total number of casualties across the DB?*/

Select SUM(number)
	From HumanImpact
	Where crisis_id in
	(Select district id as crisis_id
		From Crisis
                 Where kind = 'Death');

/*18. What is the most common type/kind of crisis occurring in the DB?*/

Select R.name
	From CrisisKind as R join Crisis as S
	On R.id = S.id
	Where count(S.kind) > ALL); 

/*19. Create a list of telephone numbers, emails, and other contact info for all orgs*/

Select name, telephone, fax, email, street_address, locality, region, postal_code,country
     From Organization;

/*20. What is the longest-lasting crisis? (if no end date, then ignore)*/

Select name
     From Crisis as R join Crisis as S 
     Where end_date is not NULL AND max(S.end_date - R.state_date);

/*21. Which person(s) is involved or associated with the most organizations?*/

Select name
	From Person
	Where id in 
	(Select person_id as id
	    From OrganizationPerson
	    Where count(person_id) > ALL);

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

Select name, kind
     From Person
     Where person_id in
	(Select id as person_id
	    From Location
	    Where (country = 'United States') OR (country = 'USA') OR (country = 'United States of America')
            Order by kind asc;

/*26. Who has the longest name?*/

Select name
	From Person
	Where max(length(first_name) + length(middle_name) + length(last_name));

/*27. Which kinds of crisis only have one crisis example?*/

Select S.kind
	From Crisis as R join CrisisKind as S
	On R.kind = S.id
	Where count(R.kind) = 1;

/*28. Which people don't have a middle name?*/

Select name
     From Person
     Where middle_name is NULL;

/*29. What are the names that start with 'B'?*/

Select name
      From Person
      Where FirstName LIKE 'B%';

/*30. List all the people associated with each country.*/

Select name, country
    From Person natural join Location
    Order by country;

/*31. What crisis affected the most countries?*/

Select country
	From Location natural join Crisis
	Where max(count(id));

/*32.What is the first (earliest) crisis in the database?*/

Select name
	From Crisis
	Where min(start_date);

/*33. What is the number of organizations in the US?*/

Select count()
	From Organization natural join Location
	Where Location = 'US';

/*34.How many people are singers?*/

Select count()
	From Person
	Where kind = 'SNG';

/*35.What is the number of leaders (current and former)? (PersonKind is "LD")*/

Select count()
	From Person
	Where kind = 'LD';

/*36. Find the start date of every hurricane that occurred in the US*/

Select state_date, name
	From Crisis natural join Location
	Where kind = 'HU' AND (country = 'United States' OR country = 'US' OR country = 'United States of America');

/*37. Number of natural disasters occurring from June 5th 2000 to June 5th 2012*/

Select count(*)
	From Crisis 
	Where kind= 'EQ' OR 'FR' OR "FL' OR 'HU' OR 'ME' OR 'ST' OR 'TO' OR 'TS' OR 'VO' 
	and start_date > 2000-06-05 AND start_date < 2012-06-05 ;

/*38. Number of political figures grouped by country.*/

Select count(*)
	From Person natural join Location
	Where kind = 'DI' OR 'FRC' OR 'GO' OR 'GOV' OR 'PO' OR 'PR' OR 'PM' OR 'SA' OR 'AMB' OR 'VP'
        Group by country;

/*39.Location with the most number of natural disasters*/

Select Country, count(*)
	From Location
	Where id in
		(select id 
			From Crisis
			Where kind = 'EQ' OR 'FR' OR "FL' OR 'HU' OR 'ME' OR 'ST' OR 'TO' OR 'TS' OR 'VO');
	Group by Country;

/*40.Average number of deaths caused by hurricanes.*/

Select avg(number)
	From HumanImpact join Crisis
	On HumanImpact.crisis_id = Crisis.id
	Where kind = "HU' AND type = 'Death';

/*41. Total number of deaths caused by terrorist attacks*/

select sum(number)
	From HumanImpact
	Where crisis_id in 
		(Select id as crisis_id
			From Crisis
			Where kind = 'TA')
	and type = 'Death';

/*42. List of Hurricanes in the US that Wallace Stickney (WStickney) helped out with.*/

Select name
	From Crisis
	Where kind= 'HU' AND id in 
		(select id_crisis as id
			From PersonCrisis
			Where id_person = 'WStickney');

/*43.List of hurricanes in the US where FEMA was NOT involved.*/

Select name
	From Crisis join CrisisOrganization
	on Crisis.id = CrisisOrganization.id_Crisis
	Where kind = 'HU' AND id_organization != 'FEMA';


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
