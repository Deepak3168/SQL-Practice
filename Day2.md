# SQL Practice Sheet: JOINs, Subqueries, CTEs, Indexes, Transactions, ACID & Normalization

**Database:** `school.db`  
**Level:** Beginner to intermediate  
**Goal:** Understand how relational data works, write SQL independently, inspect query results, and explain why each query behaves as it does.

## Instructions

1. Write the SQL yourself before checking examples.
2. Predict the output before running each query.
3. Run the query and inspect the result.
4. Explain which rows are preserved and why.
5. Unless a task explicitly asks you to, do not modify existing school records.
6. Adapt column names to your actual schema.

---

# Part A — Inspect the schema and prepare the sports tables

## A1. Inspect your existing tables

The worksheet assumes these existing tables:

- `Students(student_id, full_name, gender, class_name, section, village, age, blood_group)`
- `Subjects(subject_id, subject_name)`
- `Exams(exam_id, exam_name)`
- `Marks(mark_id, student_id, subject_id, exam_id, marks_obtained, max_marks)`

Check the actual schema first:

```sql
.tables

PRAGMA table_info(Students);
PRAGMA table_info(Subjects);
PRAGMA table_info(Exams);
PRAGMA table_info(Marks);
```

If your database uses `id` rather than `student_id`, or uses different column names, adapt your queries.

## A2. Add the sports schema

Use these two additional tables to model sports participation:

- `Sports(sport_id, sport_name, category)`
- `StudentSports(student_id, sport_id, joined_on, role)`

A student may play multiple sports, and a sport may have multiple students. Some students may play no sports, and some sports may have no registered players. `StudentSports` is the junction table that connects students and sports.

Create the tables if they do not already exist:

```sql
CREATE TABLE IF NOT EXISTS Sports (
    sport_id INTEGER PRIMARY KEY,
    sport_name TEXT NOT NULL UNIQUE,
    category TEXT
);

CREATE TABLE IF NOT EXISTS StudentSports (
    student_id INTEGER NOT NULL,
    sport_id INTEGER NOT NULL,
    joined_on TEXT,
    role TEXT,

    PRIMARY KEY (student_id, sport_id),

    FOREIGN KEY (student_id)
        REFERENCES Students(student_id),

    FOREIGN KEY (sport_id)
        REFERENCES Sports(sport_id)
);
```

Enable foreign-key enforcement for the current SQLite connection:

```sql
PRAGMA foreign_keys = ON;
```

Inspect the new tables:

```sql
PRAGMA table_info(Sports);
PRAGMA table_info(StudentSports);
```

Insert a few sports. `INSERT OR IGNORE` avoids duplicating sports if you run this setup more than once:

```sql
INSERT OR IGNORE INTO Sports (sport_name, category)
VALUES
    ('Cricket', 'Outdoor'),
    ('Football', 'Outdoor'),
    ('Basketball', 'Outdoor'),
    ('Badminton', 'Indoor'),
    ('Chess', 'Indoor'),
    ('Volleyball', 'Outdoor'),
    ('Kabaddi', 'Outdoor'),
    ('Table Tennis', 'Indoor');
```

Add example participation records. These are sample assignments, not claims about the students' actual interests:

```sql
INSERT OR IGNORE INTO StudentSports
    (student_id, sport_id, joined_on, role)
VALUES
    (1, 1, '2026-06-01', 'Batsman'),
    (1, 4, '2026-06-05', 'Singles'),
    (2, 1, '2026-06-01', 'Bowler'),
    (2, 6, '2026-06-08', 'Setter'),
    (5, 5, '2026-06-03', 'Player'),
    (8, 2, '2026-06-10', 'Goalkeeper'),
    (12, 7, '2026-06-12', 'Raider'),
    (15, 3, '2026-06-15', 'Guard'),
    (20, 8, '2026-06-18', 'Singles');
```

If your student IDs do not include these values, change the sample IDs to existing students. To find available IDs:

```sql
SELECT student_id, full_name
FROM Students
ORDER BY student_id;
```

Check the sports data:

```sql
SELECT * FROM Sports;
SELECT * FROM StudentSports;
```

**Important:** The foreign-key declarations do not automatically guarantee enforcement in every SQLite connection. Enable `PRAGMA foreign_keys = ON` for each connection that needs it. Do not insert invalid IDs just to demonstrate unmatched joins.

---

# Part B — INNER JOIN

An `INNER JOIN` returns matching row combinations from both tables. In SQLite, `JOIN` by itself means `INNER JOIN`.

Use the school tables.

1. Display each student's name and their recorded marks.
2. Display student name, subject name, and marks obtained.
3. Display student name, exam name, subject name, marks obtained, and maximum marks.
4. Display students who have at least one record in `Marks`.
5. Display students who scored more than 80, along with subject and exam names.
6. Display all results for one chosen subject.
7. Display all results for one chosen exam.
8. Join `Students` and `Marks` using table aliases (`s` and `m`).
9. Join all four school tables and sort by student name, exam name, and subject name.
10. Explain why a student with several mark records can appear several times.

**Challenge:** Write task 3 without aliases, then rewrite it using aliases.

---

# Part C — LEFT JOIN

A `LEFT JOIN` preserves every row from the left table. When there is no matching row on the right, the right-side columns appear as `NULL` in the result.

## Students and marks

11. Display every student and any matching mark records, including students without marks.
12. Find students who have no rows in `Marks`.
13. Display every subject, including subjects with no recorded marks.
14. Display every exam, including exams with no recorded marks.
15. Display every student and their marks, but keep only students from a chosen village while preserving students without marks.
16. Show each student and the number of mark records they have, including students with zero records.
17. Show every subject and the number of marks recorded for it, including subjects with zero records.
18. Explain why `COUNT(*)` and `COUNT(m.mark_id)` can give different results in a `LEFT JOIN`.

**Hint for unmatched rows:** After a `LEFT JOIN`, test a non-nullable right-side key, for example `m.mark_id IS NULL`.

## Students and sports

19. Display every student and their sport names, including students who do not play any sport.
20. Find students who do not play any sport using `LEFT JOIN` and `IS NULL`.
21. Display every sport and its participating students, including sports with no registered players. Put `Sports` on the left.
22. Display each student's name and the number of sports they play, including students who play zero sports.
23. Display every sport and its player count, including sports with zero players. Sort by player count descending.
24. Display students who play Cricket. Then change the query so every student appears, showing `NULL` when they do not play Cricket.
25. Display every student and their sport names, but match only sports in the `Outdoor` category. Preserve students with no outdoor sport.
26. Find students who play at least two different sports using `GROUP BY` and `HAVING`.
27. Explain why `COUNT(*)` and `COUNT(ss.sport_id)` can produce different counts in a `LEFT JOIN`.

## `ON` versus `WHERE` with LEFT JOIN

A condition on the right-side table placed in `WHERE` can remove unmatched rows. Compare these queries:

```sql
-- Approach 1: condition is part of the match
SELECT s.full_name, m.marks_obtained
FROM Students AS s
LEFT JOIN Marks AS m
    ON s.student_id = m.student_id
   AND m.marks_obtained >= 80;
```

```sql
-- Approach 2: condition filters the completed result
SELECT s.full_name, m.marks_obtained
FROM Students AS s
LEFT JOIN Marks AS m
    ON s.student_id = m.student_id
WHERE m.marks_obtained >= 80;
```

28. Explain why these queries can return different results.
29. Rewrite the same comparison for `Students` and `StudentSports`: preserve every student but match only their `Outdoor` sports. Then move the category condition from `ON` to `WHERE` and explain the difference.

---

# Part D — RIGHT JOIN and FULL OUTER JOIN

A `RIGHT JOIN` preserves every row from the right table and matches rows from the left where possible. A `FULL OUTER JOIN` preserves all rows from both tables, matching where possible.

SQLite supports `RIGHT JOIN` and `FULL OUTER JOIN` from version 3.39.0 onward. Check your version:

```sql
SELECT sqlite_version();
```

If your SQLite version is older, rewrite a `RIGHT JOIN` by reversing the table order and using `LEFT JOIN`. A `FULL OUTER JOIN` can be simulated with a `LEFT JOIN` plus unmatched rows from the other side, using `UNION ALL`.

## RIGHT JOIN: school tables

30. Display every mark record and its matching student's name, if available, using `RIGHT JOIN`.
31. Rewrite task 30 as a `LEFT JOIN` by reversing the table order. Compare the results.
32. Display every subject, including subjects without marks, using `RIGHT JOIN`. Which table belongs on the right?
33. Rewrite task 32 using `LEFT JOIN`. Which table should appear on the left?
34. Display every exam and its mark records, preserving exams without results.
35. For each query above, identify which table's rows must all be preserved.

## RIGHT JOIN: sports tables

36. Display every sport and its participating students using `RIGHT JOIN`, with `Sports` on the right.
37. Rewrite task 36 using `LEFT JOIN` by reversing the table order. Explain why the result should be equivalent.
38. Display every participation record and its matching student's name, preserving every row from `StudentSports` even if the student is missing.
39. Display every participation record and its matching sport name, preserving every row from `StudentSports`.
40. Compare `Students LEFT JOIN StudentSports` with `Students RIGHT JOIN StudentSports`. Explain which rows each query preserves.
41. Explain how foreign-key enforcement affects whether orphaned rows should exist in `StudentSports` or `Marks`. Why might outer joins still be useful when inspecting imported or imperfect data?

## FULL OUTER JOIN

42. Display all matching and unmatched rows from `Students` and `StudentSports` using `FULL OUTER JOIN`.
43. Display all matching and unmatched rows from `Sports` and `StudentSports` using `FULL OUTER JOIN`.
44. Compare the output of `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, and `FULL OUTER JOIN` on the same pair of tables.
45. Explain why `FULL OUTER JOIN` can return rows that are absent from both the `INNER JOIN` and one of the unmatched-only results.
46. Why can a full outer join show `NULL` values even when the original columns are declared `NOT NULL`?
47. Draw a Venn diagram for `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, and `FULL OUTER JOIN`. Label the preserved regions.

**Discussion:** In a well-designed database with enforced foreign keys, orphaned child rows should not normally exist. However, unmatched parent rows—such as students with no marks or sports with no players—are normal and useful to inspect.

---

# Part E — SELF JOIN using Employees

A self join gives the same table two aliases so its rows can be compared with other rows in that same table.

Assume you have created an `Employees` table with columns such as `employee_id`, `employee_name`, `job_title`, `department`, `salary`, and `teacher_id`.

48. Display each employee alongside their teacher/manager's name.
49. Display employee name, employee job title, manager name, and manager job title.
50. Display only employees who have a teacher/manager assigned.
51. Display employees who have no teacher/manager assigned.
52. Find employees who work in the same department as their manager.
53. Find employees who earn more than their teacher/manager.
54. Display each manager's name and the number of employees reporting directly to them.
55. Display every employee and their manager, including employees without a manager.
56. Explain why the query needs two aliases for `Employees`.
57. Change the sample data mentally: what would happen if employee 2 had `teacher_id = 4`? What hierarchy issue might this create?

**Starter query:**

```sql
SELECT
    e.employee_name AS employee,
    m.employee_name AS teacher_or_manager
FROM Employees AS e
LEFT JOIN Employees AS m
    ON e.teacher_id = m.employee_id;
```

Here, `e` represents the employee row and `m` represents the referenced teacher/manager row.

---

# Part F — The same question using different approaches

These exercises ask for similar outputs, but the correct approach depends on what rows must be preserved.

58. List students who have marks. Solve using `INNER JOIN`, then solve using `EXISTS`. Explain the difference in intent.
59. List all students and any marks using `LEFT JOIN`.
60. List subjects that have no recorded marks using `LEFT JOIN ... IS NULL`, then using `NOT EXISTS`.
61. List all exams and their mark-record counts, including exams with zero records. Use `LEFT JOIN` and `GROUP BY`.
62. Write a query showing student name and marks for a chosen exam. Compare a JOIN-based query with a subquery-based query.
63. For each student, show whether they have at least one mark record. Try `CASE WHEN EXISTS (...) THEN ... END`.
64. List all students and their sports using `LEFT JOIN`. Explain why `INNER JOIN` would omit students who do not play sports.
65. List sports that have no players using `LEFT JOIN ... IS NULL`, then solve the problem using `NOT EXISTS`.
66. Find students who play more than one sport. Compare a `JOIN` with `GROUP BY` against a query using a correlated subquery.
67. For a requirement to keep every row from one table, explain how to decide whether `LEFT JOIN`, `RIGHT JOIN`, or `FULL OUTER JOIN` is appropriate.

Do not force a `RIGHT JOIN` into a query if a clearer `LEFT JOIN` or `EXISTS` expresses the requirement better.

---

# Part G — Subqueries

A subquery is a query nested inside another SQL statement. It can return a single value, a list of values, or a result set.

68. Find students whose marks are above the overall average mark.
69. Find mark records whose marks are above the average for their own subject.
70. Find students who scored the highest mark in any subject.
71. Find students who have at least one mark record using `EXISTS`.
72. Find students who have no mark records using `NOT EXISTS`.
73. Find subjects that have at least one mark record using `IN`.
74. Find students whose mark is greater than the mark obtained by a chosen student in the same subject, if comparable records exist.
75. Find the student or students with the highest average recorded marks.
76. Compare a subquery using `IN` with one using `EXISTS`. What changes when the subquery can return multiple rows?
77. Explain why `NOT IN` can behave unexpectedly when the subquery returns `NULL`. Try `NOT EXISTS` as an alternative.
78. Find sports with no participating students using a correlated `NOT EXISTS` subquery.
79. Find students who play every sport in a chosen category. Consider whether `NOT EXISTS` can help express this requirement.

---

# Part H — Common Table Expressions (CTEs)

A CTE uses `WITH` to name a temporary result set for one SQL statement. It can make complex queries easier to read; it does not automatically make a query faster.

80. Create a CTE called `StudentResults` containing student name, subject name, exam name, marks obtained, and maximum marks. Query it to show scores above 80.
81. Create a CTE that calculates each student's average marks, then display students whose average is above 75.
82. Create a CTE that counts marks per subject, including subjects with zero records.
83. Create a CTE for employees and their manager names, then filter it to show employees in the Science department.
84. Write a query using two CTEs: one for each student's average and another for the overall average. Display students whose average exceeds the overall average.
85. Create a CTE that counts sports per student, including students with zero sports.
86. Create a CTE that counts players per sport, including sports with zero players.
87. Rewrite one query from Part G using a CTE. Explain which version is easier for you to understand and why.

---

# Part I — Indexing

An index is an additional data structure that can help SQLite find rows without scanning the whole table. Indexes can speed up reads, but take storage and can slow down inserts, updates, and deletes.

Use `EXPLAIN QUERY PLAN` to inspect query plans.

88. Inspect the query plan for finding a student by `student_id`.
89. Create an index on `Marks(student_id)`. Run `EXPLAIN QUERY PLAN` for a query filtering marks by student ID.
90. Create an index on `Marks(subject_id)`. Inspect the query plan for a subject filter.
91. Create a composite index on `Marks(subject_id, exam_id)`. Inspect a query filtering by both columns.
92. Compare a query filtering by `subject_id` alone with one filtering by `exam_id` alone. Explain why the order of columns in a composite index matters.
93. Use `PRAGMA index_list('Marks');` to list indexes on the table.
94. Use `DROP INDEX` to remove one of the indexes you created for practice.
95. Explain why creating an index on every column is not a good default strategy.
96. Consider frequent queries that find all sports for a student or all students in a sport. Which columns or column combinations in `StudentSports` could benefit from indexes? Inspect its existing primary-key index first.

Example:

```sql
CREATE INDEX IF NOT EXISTS idx_marks_student_id
ON Marks(student_id);

EXPLAIN QUERY PLAN
SELECT *
FROM Marks
WHERE student_id = 1;
```

**Note:** A small classroom database may still use a table scan. The planner's choice depends on table size, statistics, selectivity, and SQLite version. Do not judge index usefulness only by a tiny dataset.

---

# Part J — Transactions

A transaction groups statements so they can be committed together or rolled back together.

**Safety:** Use a scratch database or only the demonstration statements below. Never experiment with destructive transactions on important data.

97. Start a transaction, insert a test employee, then `ROLLBACK`. Verify that the inserted row is absent.
98. Start a transaction, insert a test employee, then `COMMIT`. Verify that the row remains.
99. Begin a transaction, update a test employee's salary, inspect the change, and roll it back.
100. Explain the difference between `COMMIT` and `ROLLBACK`.
101. What should an application do if the second of three related statements fails before the transaction commits?

Example:

```sql
BEGIN TRANSACTION;

INSERT INTO Employees
    (employee_id, employee_name, job_title, department, salary, teacher_id)
VALUES
    (100, 'Transaction Test', 'Intern', 'Testing', 20000, NULL);

ROLLBACK;

SELECT *
FROM Employees
WHERE employee_id = 100;
```

The final query should return no row because the insertion was rolled back.

---

# Part K — ACID

ACID describes four important transaction properties.

102. **Atomicity:** If an operation requires three changes and the third fails, why might we want the first two changes rolled back?
103. **Consistency:** Give two database constraints that help keep school data valid.
104. **Isolation:** If two users update the same record concurrently, what problems could arise without suitable isolation?
105. **Durability:** After a transaction is committed, what should happen if the application closes? What about a power failure, and why do storage configuration and hardware matter?
106. For each of the four examples above, label the relevant ACID property and explain why.
107. Explain why ACID is not another SQL command like `SELECT` or `CREATE`.

---

# Part L — Normalization

Normalization organizes relational data to reduce avoidable duplication and update anomalies. Use the examples below as design exercises; do not alter the original school tables.

108. Consider this table:

| student_id | student_name | subject_1 | subject_2 |
|---:|---|---|---|
| 1 | Anil | Maths | Science |
| 2 | Bhavya | English | Maths |

What problems arise when students can take a variable number of subjects? Redesign it using separate student and enrollment/result tables.

109. Consider storing `student_id`, `student_name`, `subject_id`, `subject_name`, `exam_id`, `exam_name`, and `marks` in one large table. Identify which values would be repeated across many rows.
110. Explain **1NF** using the rule that each cell should hold one value from the relevant domain, rather than a comma-separated list of subjects.
111. Explain **2NF**: why should a non-key attribute depend on the whole candidate key rather than only part of a composite key?
112. Explain **3NF**: why might `exam_name` belong in `Exams` rather than repeated in every mark record?
113. Identify an insertion anomaly, an update anomaly, and a deletion anomaly in an unnormalized school-results table.
114. Sketch a normalized design using `Students`, `Subjects`, `Exams`, and `Marks`. Identify each primary key and foreign key.
115. Explain why `StudentSports` is needed instead of storing multiple sport names in one `Students` column.
116. Discuss one trade-off of normalization: why can retrieving a full report require several JOINs?

---

# Part M — Final review

117. Explain the difference between `JOIN`/`INNER JOIN` and `LEFT JOIN` in your own words.
118. When is `LEFT JOIN ... IS NULL` useful?
119. What is the difference between `LEFT JOIN`, `RIGHT JOIN`, and `FULL OUTER JOIN`?
120. What makes a self join different from a regular join?
121. Why can one student appear multiple times in a JOIN result?
122. When would you choose a subquery versus a CTE?
123. What does an index help with, and what does it cost?
124. What does a transaction protect?
125. Name the four ACID properties.
126. What kinds of redundancy and anomalies does normalization aim to reduce?
127. Why can a `LEFT JOIN` return `NULL` in a column that is declared `NOT NULL` in the original table?
128. With 58 students and 8 sports, why might joining students to sports participation produce more than 58 rows?

---

## Suggested class sequence

1. `INNER JOIN` → `LEFT JOIN` → `RIGHT JOIN` → `FULL OUTER JOIN`
2. Sports many-to-many relationship and `StudentSports`
3. Self join with `Employees`
4. Subqueries → CTEs
5. Indexes and `EXPLAIN QUERY PLAN`
6. Transactions → ACID
7. Normalization

## Teaching reminder

Ask students to state the expected output before writing SQL. For every JOIN, they should identify:

- Which two tables are being joined?
- Which columns are used for matching?
- Which table's rows must all be preserved?
- What happens when no matching row exists?
- Could one row match several rows and therefore appear multiple times?

**Core mental model:** `INNER JOIN` keeps matches; `LEFT JOIN` keeps all left rows; `RIGHT JOIN` keeps all right rows; `FULL OUTER JOIN` keeps all rows from both sides. `NULL` in an outer-join result can mean there was no matching row—it does not necessarily mean the stored value itself was `NULL`.
'''

path = Path("/mnt/data/school_sql_practice_sheet_updated.md")
path.write_text(content, encoding="utf-8")
print(f"Created: {path}\nSize: {path.stat().st_size:,} bytes\nQuestions: 128")
