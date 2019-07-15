# Starbucks_Promotional_Offer


## Installations
1. python3: pandas, numpy


## Motivation
There are three types of offers: 
- Buy-one-get-one (BOGO): a user gets a reward equal to the threshold amount by spending a certain amount
- Discount: a user gets a reward equal to a fraction of the amount spent
- Informational: there is no reward, and neither a requisite amount that
the user needs to spend

Offers can be delivered via multiple channels. To better offer offers, we need to be clear of at least the following two things.
1. identify which groups of people are most responsive to each
type of offer
1. figure out how best to present each type of offer.


## File Description
1. Data
The data is contained in three files:

* portfolio.json - containing offer ids and meta data about each offer (duration, type, etc.) (10 offers x 6 fields)
* profile.json - demographic data for each customer (17000 users x 5 felds)
* transcript.json - records for transactions, offers received, offers viewed, and offers completed (306648 events x 4 fields)

Here is the schema and explanation of each variable in the files:

**portfolio.json**
* id (string) - offer id
* offer_type (string) - type of offer ie BOGO, discount, informational
* difficulty (int) - minimum required spend to complete an offer
* reward (int) - reward given for completing an offer
* duration (int) - time for offer to be open, in days
* channels (list of strings)

**profile.json**
* age (int) - age of the customer 
* became_member_on (int) - date when customer created an app account
* gender (str) - gender of the customer (note some entries contain 'O' for other rather than M or F)
* id (str) - customer id
* income (float) - customer's income

**transcript.json**
* event (str) - record description (ie transaction, offer received, offer viewed, etc.)
* person (str) - customer id
* time (int) - time in hours since start of test. The data begins at time t=0
* value - (dict of strings) - either an offer id or transaction amount depending on the record


### Licensing, Authors, Acknowledgements
Data used are provided by Udacity.