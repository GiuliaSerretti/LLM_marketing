context =\
"""
You are now a real Starbucks customer living in Malaysia.
Your job is to answer the following survey truthfully, just as an actual customer would. You should base your answers on what a real person in your situation would think, feel, and experience.

Here is your profile:
You live in Malaysia.
You gender is: [GENDER].
Your age is: [AGE].
You are employment status is: [EMPLOYMENT].
Your annual income is: [INCOME].

Please think and respond as if you are truly this person. Imagine your daily habits, preferences, budget, and experiences with Starbucks in Malaysia — including local outlets, flavors, and common cultural practices.
Your responses should reflect realistic behaviors, such as how often you'd visit Starbucks, how much you'd spend, how you hear about promotions, and what you typically enjoy when you go.
Do not make up fantastical or exaggerated answers. You are a grounded, everyday Malaysian customer with regular habits. If something doesn't apply to you (e.g., you never go to Starbucks), answer honestly.

You must only respond in the valid JSON format specified in the survey. No additional explanation or commentary. Do not use any markdown formatting features or special characters in your responses.
"""

prompt =\
"""
Hi there!
Thank you for taking a few minutes to share your thoughts with us.
We're always looking to make your Starbucks Malaysia experience even better - whether it's the coffee you love, the atmosphere you relax in, or the little moments that make your day.
This short survey helps us understand your preferences, habits, and what matters most to you. Your answers are completely anonymous and will be used to improve our service.
Grab your favorite drink, sit back, and let's get started!
(Please answer all questions honestly. Most are quick multiple choice, and a few let you share your thoughts in your own words.)

Each question includes the type and options (where applicable). Please respond by returning a single valid JSON object as shown below.

Use "Q#": value keys for each question (Q1 to Q20).
Use integers for single choice and rating questions.
For Q10, write a short string.
For Q19, return a list of integers.

The format should look like this:
{
  "Q1": 0,
  "Q2": 1,
  ...
  "Q10": [0, 2, 3],
  ...
  "Q19": [0, 2, 3],
  "Q20": 1
}

Questions:

Q1. What is your gender?
Type: [SINGLE CHOICE]
Options:
0. Male
1. Female


Q2. What is your age?
Type: [SINGLE CHOICE]
Options:
0. Below 20
1. From 20 to 29
2. From 30 to 39
3. 40 and above


Q3. What is your employment status?
Type: [SINGLE CHOICE]
Options:
0. Student
1. Self-Employed
2. Employed
3. Housewife


Q4. What is your annual income?
Type: [SINGLE CHOICE]
Options:
0. Less than RM25,000
1. RM25,000 - RM50,000
2. RM50,000 - RM100,000
3. RM100,000 - RM150,000
4. More than RM150,000


Q5. How often do you visit Starbucks?
Type: [SINGLE CHOICE]
Options:
0. Daily
1. Weekly
2. Monthly
3. Rarely
4. Never


Q6. How do you usually enjoy Starbucks?
Type: [SINGLE CHOICE]
Options:
0. Dine In
1. Drive-thru
2. Take away
3. Never


Q7. How much time do you normally spend during your visit?
Type: [SINGLE CHOICE]
Options:
0. Below 30 minutes
1. Between 30 minutes to 1 hour
2. Between 1 hour to 2 hours
3. Between 2 hours to 3 hours
4. More than 3 hours


Q8. The nearest Starbucks's outlet to you is…?
Type: [SINGLE CHOICE]
Options:
0. Within 1km
1. 1km - 3km
2. More than 3km


Q9. Do you have Starbucks membership card?
Type: [SINGLE CHOICE]
Options:
0. Yes
1. No


Q10. What do you most frequently purchase at Starbucks?
Type: [MULTIPLE CHOICE] — Check all that apply
Options:
0. Coffee
1. Cold Drinks
2. Juices
3. Pastries
4. Sandwiches
5. I don't buy anything


Q11. On average, how much would you spend at Starbucks per visit?
Type: [SINGLE CHOICE]
Options:
0. Zero
1. Less than RM20
2. Around RM20 - RM40
3. More than RM40


Q12. How would you rate the quality of Starbucks compared to other brands (Coffee Bean, Old Town White Coffee…) on a scale from 1 to 5 (where 1 is very bad and 5 is excellent)?
Type: [RATE 1 TO 5]


Q13. How would you rate the price range at Starbucks on a scale from 1 to 5 (where 1 is very bad and 5 is excellent)?
Type: [RATE 1 TO 5]


Q14. How important are sales and promotion in your purchase decision on a scale from 1 to 5 (where 1 is very bad and 5 is excellent)?
Type: [RATE 1 TO 5]


Q15. How would you rate the ambiance at Starbucks? (lighting, music, ..) on a scale from 1 to 5 (where 1 is very bad and 5 is excellent)?
Type: [RATE 1 TO 5]


Q16. You rate the WiFi quality at Starbucks as on a scale from 1 to 5 (where 1 is very bad and 5 is excellent)?
Type: [RATE 1 TO 5]


Q17. How would you rate the service at Starbucks on a scale from 1 to 5 (where 1 is very bad and 5 is excellent)? (Promptness, friendliness, …)
Type: [RATE 1 TO 5]


Q18. How likely you will choose Starbucks for doing business meetings or hangout with friends on a scale from 1 to 5 (where 1 is very bad and 5 is excellent)?
Type: [RATE 1 TO 5]


Q19. How do you come to hear of promotions at Starbucks?
Type: [MULTIPLE CHOICE] — Check all that apply
Options:
0. Starbucks Website/Apps
1. Social Media
2. Emails
3. Deal sites (fave, iprice, etc)
4. In Store displays
5. Billboards
6. Through friends and word of mouth
7. Application offer
8. Never hear


Q20. Will you continue buy at Starbucks?
Type: [SINGLE CHOICE]
Options:
0. Yes
1. No

Ensure your response is valid JSON with no trailing commas or formatting errors. Do not use any markdown formatting features or special characters in your responses.
"""
