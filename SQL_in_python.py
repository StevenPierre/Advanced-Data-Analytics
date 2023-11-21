Problem 9: SQL Operations
This problem will test your ability to manipulate two simple SQL tables. You may find a problem easier to complete using Pandas, or you may find a problem easier to complete in SQL. We will provide you will a SQLite database containing two tables, and two Pandas Dataframes that are identical to the SQLite tables.

import sys
import pandas as pd
import sqlite3 as db
from IPython.display import display

def get_data_path(filebase):
    return f"resource/asnlib/publicdata/movies/{filebase}"

print(f"* Python version: {sys.version}")
print(f"* pandas version: {pd.__version__}")
print(f"* sqlite3 version: {db.version}")
* Python version: 3.7.5 (default, Dec 18 2019, 06:24:58) 
[GCC 5.5.0 20171010]
* pandas version: 1.1.2
* sqlite3 version: 2.6.0
The Movies and Cast Dataset
The data consists of two tables. The first is a table of movies along with (random) audience scores from 1-100. The second is a table of cast members for those movies. There are some interesting cast members in here that you might stumble upon!

Let's read in the database file and show the table descriptions.

disk_engine = db.connect(get_data_path('movieDB.db'))
c = disk_engine.cursor()

c.execute('SELECT type, name, sql FROM sqlite_master')
results = c.fetchall()
for table in results:
    print(table)
('table', 'movies', 'CREATE TABLE movies (id integer, name text, score integer)')
('table', 'cast', 'CREATE TABLE cast (movie_id integer, cast_id integer, cast_name text)')
movies = pd.read_table(get_data_path('movie-name-score.txt'), sep=',', header=None, names=['id', 'name', 'score'])
cast = pd.read_table(get_data_path('movie-cast.txt'), sep=',', header=None, names=['movie_id', 'cast_id', 'cast_name'])

print('Movies Dataframe:')
print('-------------------')
display(movies.head())
print('\n\n')
print('Cast Dataframe:')
print('-------------------')
display(cast.head())
Movies Dataframe:
-------------------
id	name	score
0	9	Star Wars: Episode III - Revenge of the Sith 3D	61
1	24214	The Chronicles of Narnia: The Lion, The Witch ...	46
2	1789	War of the Worlds	94
3	10009	Star Wars: Episode II - Attack of the Clones 3D	28
4	771238285	Warm Bodies	3


Cast Dataframe:
-------------------
movie_id	cast_id	cast_name
0	9	162652153	Hayden Christensen
1	9	162652152	Ewan McGregor
2	9	418638213	Kenny Baker
3	9	548155708	Graeme Blundell
4	9	358317901	Jeremy Bulloch
In terms of Database structures, the cast table's movie_id column is a foreign key to the movie table's id column.

This means you can perform any SQL joins or Pandas merges between the two tables on this column.

One final code cell to get you started - implement the all-too-familiar canonicalize_tibble and tibbles_are_equivalent functions.

def canonicalize_tibble(X):
    var_names = sorted(X.columns)
    Y = X[var_names].copy()
    Y.sort_values(by=var_names, inplace=True)
    Y.reset_index(drop=True, inplace=True)
    return Y

def tibbles_are_equivalent (A, B):
    A_canonical = canonicalize_tibble(A)
    B_canonical = canonicalize_tibble(B)
    equal = (A_canonical == B_canonical)
    return equal.all().all()
Let's start with two warm-up exercises.

Exercise 0 (2 points): Create a dataframe, cast_size, that contains the number of distinct cast members per movie. Your table will have two columns, movie_name, the name of each film, and cast_count, the number of unique cast members for the film.

Order the result by cast_count from highest to lowest.

Note: In SQL, the word cast is actually a reserved keyword, which is used to convert values from one type to another (e.g., a floating-point value to an integer). To distinguish the table named cast from the keyword, use the syntax, [cast] in SQLite when referencing the table. (This notation is not standard, and therefore might not port to other SQL implementations.

### BEGIN SOLUTION
# SQL solution: join on movie id, then count cast ids
query = ''' select name as movie_name, count(cast_id) as cast_count
            from movies inner join [cast] on id = movie_id 
            group by movie_id order by cast_count desc'''

cast_size = pd.read_sql_query(query, disk_engine)
#print(cast_size)

# Pandas solution: merge and groupby + agg
joined_df = movies.merge(cast, how='inner', left_on='id', right_on='movie_id')
cast_size2 = joined_df.groupby(['id', 'name']).size().reset_index(name='cast_count')

cast_size2 = cast_size2.sort_values(by='cast_count', ascending=False)[['name', 'cast_count']]
cast_size2.columns = ['movie_name', 'cast_count']

print(tibbles_are_equivalent(cast_size, cast_size2))
### END SOLUTION
True
display(cast_size)
movie_name	cast_count
0	The War of the Worlds	72
1	The Chronicles of Narnia: The Lion, The Witch ...	66
2	Star Wars: Episode III - Revenge of the Sith 3D	66
3	Star Wars: Episode VI - Return of the Jedi	65
4	This Means War	64
...	...	...
388	Japan's War in Colour	1
389	War of the Century - When Hitler Fought Stalin	1
390	World War 1 in Color	1
391	War Gods of the Deep	1
392	Noam Chomsky - Distorted Morality: America's W...	1
393 rows × 2 columns

# Test cell : `test_cast_size`

print("Reading instructor's solution...")

cast_size_solution = pd.read_csv(get_data_path('cast_size_solution.csv'))
display(cast_size_solution)
print("Checking...")

assert set(cast_size.columns) == {'movie_name', 'cast_count'}
assert tibbles_are_equivalent(cast_size, cast_size_solution), "Your Dataframe is incorrect"
assert all(cast_size['cast_count'] == cast_size_solution['cast_count'])


print("\n(Passed!.)")

del cast_size_solution
Reading instructor's solution...
movie_name	cast_count
0	The War of the Worlds	72
1	Star Wars: Episode III - Revenge of the Sith 3D	66
2	The Chronicles of Narnia: The Lion, The Witch ...	66
3	Star Wars: Episode VI - Return of the Jedi	65
4	This Means War	64
...	...	...
388	Diamonds of War: Africa's Blood Diamond	1
389	War - Greatest Hits Live	1
390	Imperial War Museum: The Royal Air Force at War	1
391	Visions of War: The Algerian War	1
392	War Feels Like War	1
393 rows × 2 columns

Checking...

(Passed!.)
Exercise 1 (2 point): Create a dataframe, cast_score, that contains the average movie score for each cast member. Your table will have two columns, cast_name, the name of each cast member, and avg_score, the average movie review score for each movie that the cast member appears in.

Order this result by avg_score from highest to lowest, and round your result for avg_score to two (2) decimal places.

Break any ties in your sorting by cast name in alphabetical order from A-Z.

### BEGIN SOLUTION
# SQL solution: group by and avg
query = ''' select cast_name, round(avg(score), 2) as avg_score from 
            [cast] inner join movies on movie_id = id
            group by cast_id order by avg_score desc, cast_name asc'''
cast_score = pd.read_sql_query(query, disk_engine)
#print(cast_score)

# Pandas solution: merge and group by + mean()
joined_df = cast.merge(movies, how='inner', left_on='movie_id', right_on='id')
cast_score2 = joined_df.groupby(['cast_id', 'cast_name']).mean().reset_index()
cast_score2 = cast_score2.sort_values(by=['score', 'cast_name'], ascending=[False, True])[['cast_name', 'score']]
cast_score2.columns = ['cast_name', 'avg_score']
cast_score2 = cast_score2.round(2)
print(tibbles_are_equivalent(cast_score, cast_score2))
### END SOLUTION
True
# Test cell : `test_cast_score`
print("Reading instructor's solution...")

cast_score_solution = pd.read_csv(get_data_path('cast_score_solution.csv'))

print("Checking...")

assert set(cast_score.columns) == {'cast_name', 'avg_score'}
assert tibbles_are_equivalent(cast_score, cast_score_solution), "Your Dataframe is incorrect"
assert all(cast_score['avg_score'] == cast_score_solution['avg_score'])


print("\n(Passed!)")

del cast_score_solution
Reading instructor's solution...
Checking...

(Passed!)
Exercise 2 (3 points): You will now create a dataframe, one_hit_wonders, that contains actors and actresses that appear in exactly one movie, with a movie score == 100. Your result will have three columns, cast_name, the name of each cast member that meets the criteria, movie_name, the name of the movie that cast member appears in, and movie_score, which for the purposes of this Exercise is always == 100.

Order your result by cast_name in alphabetical order from A-Z.

### BEGIN SOLUTION
# SQL solution: group by having count = 1
query = ''' select cast_name, name as movie_name, score as movie_score
            from [cast] inner join movies on movie_id = id
            group by cast_id
            having count(movie_id) = 1 and score = 100
            order by cast_name
            '''
one_hit_wonders = pd.read_sql_query(query, disk_engine)

joined_df = cast.merge(movies, how='inner', left_on='movie_id', right_on='id')
one_hit_wonders2 = joined_df.groupby(['cast_id']).filter(lambda group: len(group) == 1 and group['score'] == 100)
one_hit_wonders2 = one_hit_wonders2[['cast_name', 'name', 'score']]
one_hit_wonders2.columns = ['cast_name', 'movie_name', 'movie_score']
one_hit_wonders2.sort_values(by='cast_name', ascending=True)

print(tibbles_are_equivalent(one_hit_wonders, one_hit_wonders2))
### END SOLUTION
True
# Test cell : `one_hit_wonders_score`

print("Reading instructor's solution...")

one_hit_wonders_solution = pd.read_csv(get_data_path('one_hit_wonders_solution.csv'))

print("Checking...")

assert set(one_hit_wonders.columns) == {'cast_name','movie_name', 'movie_score'}
assert tibbles_are_equivalent(one_hit_wonders, one_hit_wonders_solution)
assert all(one_hit_wonders['movie_score'] == one_hit_wonders_solution['movie_score'])

print("\n(Passed!)")

del one_hit_wonders_solution
Reading instructor's solution...
Checking...

(Passed!)
Exercise 3 (3 points): For this problem, you will find cast members that work well together. We define this as two cast members being in >= 3 movies together, with the average movie score being >= 50.

You will create a dataframe called good_teamwork that contains four columns:

cast_member_1 and cast_member_2, the names of each pair of cast members that appear in the same movie;
num_movies, the number of movies that each pair of cast members appears in; and
avg_score, the average review score for each of those movies containing the two cast members.
Order the results by cast_member_1 alphabetically from A-Z, and break any ties by sorting by cast_member_2 alphabetically from A-Z. Round the result for avg_score to two (2) decimal places.

One more wrinkle: your solution will likely create several duplicate pairs of cast members: rows such as:

cast_member_1	cast_member_2	num_movies	avg_score
Anthony Daniels	Frank Oz	5	50.60
Frank Oz	Anthony Daniels	5	50.60
Remove all duplicate pairs, keeping all cases where cast_member_1's name comes before cast_member_2's name in the alphabet. In the example above, you will keep only the first row in your final solution. Make sure to also remove matches where cast_member_1 == cast_member_2.

### BEGIN SOLUTION
query = '''select a.cast_name as cast_member_1,
                  b.cast_name as cast_member_2,
                  count(*) as num_movies,
                  round(avg(score), 2) as avg_score
           from [cast] as a
               inner join [cast] as b on (a.movie_id = b.movie_id and a.cast_name < b.cast_name)
               inner join movies c on b.movie_id = c.id
           group by a.cast_name, b.cast_name
           having num_movies >=3 and avg_score >=50
           order by cast_member_1, cast_member_2
        '''
good_teamwork = pd.read_sql_query(query, disk_engine)

joined_df = cast.merge(cast, how='inner', left_on='movie_id', right_on='movie_id')
joined_df = joined_df.query('cast_name_x < cast_name_y')
good_teamwork2 = joined_df.merge(movies, how='inner', left_on='movie_id', right_on='id')
good_teamwork2 = good_teamwork2.groupby(['cast_name_x', 'cast_name_y']).agg({'movie_id': 'size', 'score': 'mean'}).reset_index()
good_teamwork2.rename(columns={'cast_name_x': 'cast_member_1',
                               'cast_name_y': 'cast_member_2',
                               'movie_id': 'num_movies',
                               'score': 'avg_score'},
                      inplace=True)
good_teamwork2 = good_teamwork2[good_teamwork2['avg_score'] >= 50]
good_teamwork2 = good_teamwork2[good_teamwork2['num_movies'] >= 3]
good_teamwork2 = good_teamwork2.round({'avg_score': 2})
good_teamwork2 = good_teamwork2.sort_values(by=['cast_member_1', 'cast_member_2'], ascending=[True, True]).reset_index(drop=True)
### END SOLUTION
# Test cell : `good_teamwork_score`
print("Reading instructor's solution...")

good_teamwork_solution = pd.read_csv(get_data_path('good_teamwork_solution.csv'))
print(good_teamwork_solution)

print("Checking...")

assert set(good_teamwork.columns) == {'cast_member_1','cast_member_2', 'num_movies', 'avg_score'}
assert tibbles_are_equivalent(good_teamwork, good_teamwork_solution)
assert all(good_teamwork['num_movies'] == good_teamwork_solution['num_movies'])
assert all(good_teamwork['avg_score'] == good_teamwork_solution['avg_score'])

print("\n(Passed!)")

del good_teamwork_solution
Reading instructor's solution...
         cast_member_1      cast_member_2  num_movies  avg_score
0           Ahmed Best    Anthony Daniels           3      54.67
1           Ahmed Best      Ewan McGregor           3      54.67
2           Ahmed Best           Frank Oz           3      54.67
3           Ahmed Best      Ian McDiarmid           3      54.67
4           Ahmed Best        Kenny Baker           3      54.67
..                 ...                ...         ...        ...
63     Natalie Portman  Samuel L. Jackson           3      54.67
64     Natalie Portman       Silas Carson           3      54.67
65  Oliver Ford Davies  Samuel L. Jackson           3      54.67
66  Oliver Ford Davies       Silas Carson           3      54.67
67   Samuel L. Jackson       Silas Carson           3      54.67

[68 rows x 4 columns]
Checking...

(Passed!)
c.close()
disk_engine.close()
Fin! Remember to test your solutions by running them as the autograder will: restart the kernel and run all cells from "top-to-bottom." Also remember to submit to the autograder; otherwise, you will not get credit for your hard work!
