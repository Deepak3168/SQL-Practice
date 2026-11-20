# SQL Reading Practice — Students Table Only

**Topic:** Reading data with SQL  
**Database:** `school.db`  
**Table:** `Students`  
**Allowed SQL:** `SELECT`, `WHERE`, `ORDER BY`, `DISTINCT`, `GROUP BY`, `HAVING`, and aggregate functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).

## Instructions

- Write a SQL query for every task.
- Use only the `Students` table.
- Do **not** use `JOIN`, `INSERT`, `UPDATE`, `DELETE`, or `ALTER TABLE`.
- Do not change any data.
- Unless a task says otherwise, display only the columns needed to answer it.
- Some tasks require `age` and `blood_group` columns. Complete those only if these columns have already been added to `Students`.

---

## Level 1 — SELECT

1. Display every column and every row from the `Students` table.
2. Display only each student's `full_name`.
3. Display each student's name, class, and section.
4. Display each student's name and village.
5. Display each student's name, age, and blood group.
6. Display the names and genders of all students.
7. Display the student ID and name of every student.
8. Display the name and section of every student in the table.

## Level 2 — WHERE

9. Find all students who belong to section `A`.
10. Find all students who belong to section `B`.
11. Find all students who live in `Kakinada`.
12. Find all students who live in `Rajahmundry`.
13. Find all students whose age is exactly `16`.
14. Find all students whose age is less than `17`.
15. Find all students whose age is `15` or `16`.
16. Find all students whose blood group is `O+`.
17. Find all students whose blood group is either `A+` or `B+`.
18. Find all students who are male and belong to section `A`.
19. Find all students who are female and live in `Amalapuram`.
20. Find all students whose age is greater than `15` and who belong to section `B`.
21. Find all students whose age is between `15` and `17`, inclusive.
22. Find all students whose village is not `Kakinada`.
23. Find all students whose name starts with the letter `S`.
24. Find all students whose name contains `Sri`.
25. Find all students whose name ends with `Reddy`.

## Level 3 — ORDER BY

26. Display all students in alphabetical order by name.
27. Display all students in reverse alphabetical order by name.
28. Display all students from youngest to oldest.
29. Display all students from oldest to youngest.
30. Display all students sorted by village name.
31. Display all students sorted first by section and then by name.
32. Display all students sorted by age from highest to lowest, and then by name alphabetically.
33. Display the first five students when sorted alphabetically by name.

## Level 4 — DISTINCT

34. Display each village only once.
35. Display each blood group only once.
36. Display each age value only once.
37. Display each section value only once.
38. Display each unique combination of `class_name` and `section`.
39. Display each unique combination of `village` and `blood_group`.

## Level 5 — Aggregate Functions

40. Count the total number of students.
41. Count how many students are male.
42. Count how many students are female.
43. Find the youngest student's age.
44. Find the oldest student's age.
45. Calculate the average age of all students.
46. Find the total of all students' ages.
47. Count how many students have a recorded blood group.
48. Find the average age of students in section `A`.
49. Find the minimum and maximum age among students in section `B`.
50. Count how many students live in `Kakinada`.

## Level 6 — GROUP BY

51. Count the number of students in each section.
52. Count the number of students of each gender.
53. Count the number of students in each village.
54. Count the number of students in each age group.
55. Count the number of students for each blood group.
56. Find the average age for each section.
57. Find the minimum and maximum age for each section.
58. Count students for each combination of gender and section.
59. Count students for each combination of village and section.
60. Find the average age for each blood group.

## Level 7 — HAVING

61. Display only villages that have more than three students.
62. Display only sections that have more than 20 students.
63. Display only blood groups shared by at least five students.
64. Display only age groups containing more than 10 students.
65. Display only genders with more than 20 students.
66. Display only villages with at least two female students.
67. Display only sections whose average age is greater than `16`.
68. Display only blood groups whose average age is less than `17`.
69. Display only villages whose average student age is at least `16`.
70. Display only gender-and-section groups containing at least 10 students.

## Level 8 — Mixed Challenges

71. Count students aged 16 or older.
72. Find the average age of students who live in `Kakinada`.
73. Count students in each village, showing the largest groups first.
74. Display the three villages with the highest student counts.
75. Find the average age of male students in section `A`.
76. Count female students in each village and show only villages with at least two female students.
77. Display each blood group and its student count, sorted from most common to least common.
78. Find the age group with the highest number of students.
79. Count students by section, but include only students whose age is greater than `15` before grouping.
80. For each village, count students aged 16 or older and display only villages with at least two such students.

---

## Quick Revision

- `SELECT` — choose which columns to read.
- `WHERE` — filter individual rows before grouping.
- `ORDER BY` — sort the result.
- `DISTINCT` — remove duplicate result rows.
- `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` — calculate summary values.
- `GROUP BY` — make groups of rows to summarize.
- `HAVING` — filter groups after grouping.
- `LIMIT`  — returns the limited rows 

