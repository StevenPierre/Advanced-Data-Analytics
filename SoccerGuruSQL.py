Problem 13: Soccer (a.k.a., the Real Football) Guru
Version 1.5

Soccer season is on and teams need to start preparing for the World Cup 2022. We need your help as a Soccer Guru to analyse different statistics and come up with insights to help the teams prepare better.

This problem tests your understanding of Pandas and SQL concepts.

Important note. Due to a limitation in Vocareum's software stack, this notebook is set to use the Python 3.5 kernel (rather than a more up-to-date 3.6 or 3.7 kernel). If you are developing on your local machine and are using a different version of Python, you may need to adapt your solution before submitting to the autograder.

Exercise 0 (0 points). Run the code cell below to load the data, which is a SQLite3 database containing results and fixtures of various soccer matches that have been played around the globe since 1980.

Observe that the code loads all rows from the table, soccer_results, contained in the database file, prob0.db.

You do not need to do anything for this problem other than run the next two code cells and familiarize yourself with the resulting dataframe, which is stored in the variable df.

import sqlite3 as db
import pandas as pd
from datetime import datetime
from collections import defaultdict
disk_engine = db.connect('file:resource/asnlib/publicdata/prob0.db?mode=ro', uri=True)

def load_data():
    df = pd.read_sql_query("SELECT * FROM soccer_results", disk_engine) 
    return df
# Test: Exercise 0 (exposed)
df = load_data()
assert df.shape[0] == 22851, "Row counts do not match. Try loading the data again"
assert df.shape[1] == 9, "You don't have all the columns. Try loading the data again"
print("\n(Passed!)")
df.head()
(Passed!)
date	home_team	away_team	home_score	away_score	tournament	city	country	neutral
0	1994-01-02	Barbados	Grenada	0	0	Friendly	Bridgetown	Barbados	FALSE
1	1994-01-02	Ghana	Egypt	2	1	Friendly	Accra	Ghana	FALSE
2	1994-01-05	Mali	Burkina Faso	1	1	Friendly	Bamako	Mali	FALSE
3	1994-01-09	Mauritania	Mali	1	3	Friendly	Nouakchott	Mauritania	FALSE
4	1994-01-11	Thailand	Nigeria	1	1	Friendly	Bangkok	Thailand	FALSE
Each row of this dataframe is a game, which is played between a "home team" (column home_team) and an "away team" (away_team). The number of goals scored by each team appears in the home_score and away_score columns, respectively.

Exercise 1 (1 point): Write an SQL query find the ten (10) teams that have the highest average away-scores since the year 2000. Your query should satisfy the following criteria:

It should return two columns:
team: The name of the team
ave_goals: The team's average number of goals in "away" games. An "away game" is one in which the team's name appars in away_team and the game takes place at a "non-neutral site" (neutral value equals FALSE).
It should only include teams that have played at least 30 away matches.
It should round the average goals value (ave_goals) to three decimal places.
It should only return the top 10 teams in descending order by average away-goals.
It should only consider games played since 2000 (including the year 2000).
Store your query string as the variable, query_top10_away, below. The test cell will run this query string against the input dataframe, df, defined above and return the result in a dataframe named offensive_teams. (See the test cell.)

Note. The following exercises have hidden test cases and you'll be awarded full points for passing both the exposed and hidden test cases.

query_top10_away = ''  # Write your query here!

### BEGIN SOLUTION
query_top10_away = """
SELECT away_team AS team, ROUND(AVG(away_score), 3) AS ave_goals
    FROM soccer_results
    WHERE STRFTIME('%Y', date) >= '2000' AND neutral = 'FALSE'
    GROUP BY away_team
    HAVING COUNT(*) >= 30
    ORDER BY ave_goals DESC
    LIMIT 10"""
### END SOLUTION

print(query_top10_away)
SELECT away_team AS team, ROUND(AVG(away_score), 3) AS ave_goals
    FROM soccer_results
    WHERE STRFTIME('%Y', date) >= '2000' AND neutral = 'FALSE'
    GROUP BY away_team
    HAVING COUNT(*) >= 30
    ORDER BY ave_goals DESC
    LIMIT 10
# Test: Exercise 1 (exposed)
offensive_teams = pd.read_sql_query(query_top10_away, disk_engine)
df_cols = offensive_teams.columns.tolist()
df_cols.sort()
desired_cols = ['team', 'ave_goals']
desired_cols.sort()
print(offensive_teams.head(10))
assert offensive_teams.shape[0] == 10, "Expected 10 rows but returned dataframe has {}".format(offensive_teams.shape[0])
assert offensive_teams.shape[1] == 2, "Expected 2 columns but returned dataframe has {}".format(offensive_teams.shape[1])
assert df_cols == desired_cols, "Column names should be: {}. Returned dataframe has: {}".format(desired_cols, df_cols)

tolerance = .001
team_4 = offensive_teams.iloc[3].team
team_4_ave = offensive_teams.iloc[3].ave_goals
desired_team_4_ave = 1.763
assert (team_4 == "England" and abs(team_4_ave - 1.763) <= .001), "Fourth entry is {} with average of {}. Got {} with average of {}".format("England", 1.76, team_4, team_4_ave)

print("\n(Passed!)")
           team  ave_goals
0       Germany      2.170
1        Brazil      2.010
2         Spain      1.927
3       England      1.763
4   Netherlands      1.742
5        France      1.639
6      Portugal      1.579
7     Argentina      1.560
8  Saudi Arabia      1.540
9       Denmark      1.534

(Passed!)
# Hidden test cell: exercise1_hidden

print("""
In addition to the tests above, this cell will include some hidden tests.
You will only know the result when you submit your solution to the
autograder.
""")

### BEGIN HIDDEN TESTS

sql_query = "SELECT away_team as team, round(avg(away_score), 3) as ave_goals FROM soccer_results\
              WHERE strftime('%Y', date) >= '2000' AND neutral = 'FALSE'\
              GROUP BY away_team\
              HAVING count(*) >= 30\
              ORDER BY ave_goals DESC\
              LIMIT 10"
test_df = pd.read_sql_query(sql_query, disk_engine)

offensive_teams = offensive_teams.reset_index(drop=True)
test_df = test_df.reset_index(drop=True)


merged = test_df.merge(offensive_teams, indicator=True, how='outer')
diffs = merged[merged['_merge'] == 'right_only']
assert len(diffs) == 0, "The dataframe doesn't match the expected output on \n{}".format(diffs)
assert offensive_teams.equals(test_df), "The dataframe doesn't match the expected output"

print("Passed!")
### END HIDDEN TESTS
In addition to the tests above, this cell will include some hidden tests.
You will only know the result when you submit your solution to the
autograder.

Passed!
Exercise 2 (2 points): Suppose we are now interested in the top 10 teams having the best goal differential, between the years 2012 and 2018 (both inclusive). A team's goal differential is the difference between the total number of goals it scored and the total number it conceded across all games (in the requested years).

Complete the function, best_goal_differential(), below, so that it returns a pandas dataframe containing the top 10 teams by goal differential, sorted in descending order of differential. The dataframe should have two columns: team, which holds the team's name, and differential, which holds its overall goal differential.

As a sanity check, you should find the Brazil is the number one team, with a differential of 152 during the selected time period of 2012-2018 (inclusive). It should be the first row of the returned dataframe.

def best_goal_differential():
    ### BEGIN SOLUTION
    return best_goal_differential__v1_pandas()

# Solution method 0: SQL
def best_goal_differential__v0_SQL():
    sql_query = "WITH home as (SELECT home_team, SUM((home_score-away_score)) as diff \
                    from soccer_results WHERE strftime('%Y', date) >= '2012'\
                    AND strftime('%Y', date) <= '2018' GROUP BY home_team),\
                    away as (SELECT away_team, SUM((away_score-home_score)) as diff \
                    from soccer_results WHERE strftime('%Y', date) >= '2012'\
                    AND strftime('%Y', date) <= '2018' GROUP BY away_team)\
                SELECT away_team as team, (away.diff + home.diff) as differential FROM away, home\
                WHERE away.away_team = home.home_team GROUP BY away_team ORDER BY differential DESC\
                LIMIT 10"
    df = pd.read_sql_query(sql_query, disk_engine)
    return df

# Solution method 1: Pandas
def filter_year(df, first, last=None):
    if last is None: last = first
    def limit_range(x):
        return (x[:4] >= first) and (x[:4] <= last)
    return df[df['date'].apply(limit_range)]

def best_goal_differential__v1_pandas():
    df2 = filter_year(df, '2012', '2018')
    home_total = df2.groupby('home_team')['home_score'].sum()
    home_opp_total = df2.groupby('home_team')['away_score'].sum()
    away_total = df2.groupby('away_team')['away_score'].sum()
    # print(away_total.head(5))
    away_opp_total = df2.groupby('away_team')['home_score'].sum()
    diffs = (home_total + away_total) - (home_opp_total + away_opp_total)
    print(type(diffs))
    diffs_df = diffs.sort_values(ascending=False) \
                    .to_frame() \
                    .reset_index() \
                    .rename(columns={'index': 'team', 0: 'differential'}).iloc[:10]
    diffs_df['differential'] = diffs_df['differential'].astype(int)
    # print(type(diffs_df))
    return diffs_df
    ### END SOLUTION  
# Test: Exercise 2 (exposed)

diff_df = best_goal_differential()
df_cols = diff_df.columns.tolist()
df_cols.sort()
desired_cols = ['team', 'differential']
desired_cols.sort()

assert isinstance(diff_df, pd.DataFrame), "Dataframe object not returned"
assert diff_df.shape[0] == 10, "Expected 10 rows but returned dataframe has {}".format(diff_df.shape[0])
assert diff_df.shape[1] == 2, "Expected 2 columns but returned dataframe has {}".format(diff_df.shape[1])
assert df_cols == desired_cols, "Column names should be: {}. Returned dataframe has: {}".format(desired_cols, df_cols)

best_team = diff_df.iloc[0].team
best_diff = diff_df.iloc[0].differential
assert (best_team == "Brazil" and best_diff == 152), "{} has best differential of {}. Got team {} having best differential of {}".format("Brazil", 152, best_team, best_diff)

print("\n(Passed!)")
<class 'pandas.core.series.Series'>

(Passed!)
# Hidden test cell: exercise2_hidden

print("""
In addition to the tests above, this cell will include some hidden tests.
You will only know the result when you submit your solution to the
autograder.
""")

### BEGIN HIDDEN TESTS
sql_query = "WITH home as (SELECT home_team, SUM((home_score-away_score)) as diff \
                    from soccer_results WHERE strftime('%Y', date) >= '2012'\
                    AND strftime('%Y', date) <= '2018' GROUP BY home_team),\
                    away as (SELECT away_team, SUM((away_score-home_score)) as diff \
                    from soccer_results WHERE strftime('%Y', date) >= '2012'\
                    AND strftime('%Y', date) <= '2018' GROUP BY away_team)\
                SELECT away_team as team, (away.diff + home.diff) as differential FROM away, home\
                WHERE away.away_team = home.home_team GROUP BY away_team ORDER BY differential DESC\
                LIMIT 10"
test_df = pd.read_sql_query(sql_query, disk_engine)

best_goal_differential = best_goal_differential()
best_goal_differential = best_goal_differential.reset_index(drop=True)
test_df = test_df.reset_index(drop=True)




merged = test_df.merge(best_goal_differential, indicator=True, how='outer')
diffs = merged[merged['_merge'] == 'right_only']
assert len(diffs) == 0, "The dataframe doesn't match the expected output on \n{}".format(diffs)
assert best_goal_differential.equals(test_df), "The dataframe doesn't match the expected output"

print("\nPassed!")
### END HIDDEN TESTS
In addition to the tests above, this cell will include some hidden tests.
You will only know the result when you submit your solution to the
autograder.

<class 'pandas.core.series.Series'>

Passed!
Exercise 3 (1 point). Complete the function, determine_winners(game_df), below. It should determine the winner of each soccer game.

In particular, the function should take in a dataframe like df from above. It should return a new dataframe consisting of all the columns from that dataframe plus a new columnn called winner, holding the name of the winning team. If there is no winner for a particular game (i.e., the score is tied), then the winner column should containing the string, 'Draw'. Lastly, the rows of the output should be in the same order as the input dataframe.

You can use any dataframe manipulation techniques you want for this question (i.e., pandas methods or SQL queries, as you prefer).

You'll need the output dataframe from this exercise for the subsequent exercies, so don't skip this one!

def determine_winners(game_df):
    ### BEGIN SOLUTION
    def who_won(row):
        if row['home_score'] > row['away_score']:
            return row['home_team']
        if row['home_score'] < row['away_score']:
            return row['away_team']
        return 'Draw'
    winners_df = game_df.copy()
    winners_df['winner'] = game_df.apply(who_won, axis=1)
    return winners_df
    ### END SOLUTION
# Test: Exercise 3 (exposed)

game_df = pd.read_sql_query("SELECT * FROM soccer_results", disk_engine)
winners_df = determine_winners(game_df)

game_winner = winners_df.iloc[1].winner
assert game_winner == "Ghana", "Expected Ghana to be winner. Got {}".format(game_winner)

game_winner = winners_df.iloc[2].winner
assert game_winner == "Draw", "Match was Draw. Got {}".format(game_winner)

game_winner = winners_df.iloc[3].winner
assert game_winner == "Mali", "Expected Mali to be winner. Got {}".format(game_winner)

print("\n(Passed!)")
(Passed!)
# Hidden test cell: exercise3_hidden

print("""
In addition to the tests above, this cell will include some hidden tests.
You will only know the result when you submit your solution to the
autograder.
""")

### BEGIN HIDDEN TESTS
def get_winner(row):
    home_score = row['home_score']
    away_score = row['away_score']
    winner = 'Draw'
    if home_score > away_score:
        winner = row['home_team']
    elif home_score < away_score:
        winner = row['away_team']
    
    return(winner)

def sol_3(game_df_sol):
    game_df_sol = game_df_sol.assign(winner = "None")
    dummy_df = game_df.copy()
    dummy_df['winner'] = dummy_df.apply(lambda x : get_winner(x), axis =1)
    
    return dummy_df

game_df = pd.read_sql_query("SELECT * FROM soccer_results", disk_engine)    
game_df_sol = sol_3(game_df)
winners_df = determine_winners(game_df)

winners_df = winners_df.reset_index(drop=True)
game_df_sol = game_df_sol.reset_index(drop=True)

merged = game_df_sol.merge(winners_df, indicator=True, how='outer')
diffs = merged[merged['_merge'] == 'right_only']
assert len(diffs) == 0, "The dataframe doesn't match the expected output on \n{}".format(diffs)
assert winners_df.equals(game_df_sol), "The dataframe doesn't match the expected output"

print("\nPassed!")
### END HIDDEN TESTS
In addition to the tests above, this cell will include some hidden tests.
You will only know the result when you submit your solution to the
autograder.


Passed!
Exercise 4 (3 points): Given a team, its home advantage ratio is the number of home games it has won divided by the number of home games it has played. For this exercise, we'll try to answer the question, how important is the home advantage in soccer? It's importance is factored into draws for competitions, for example, teams wanting to play at home the second leg of the matches of great importance such as tournament knockouts. (This exercise has a pre-requisite of finishing Exercise 3 as we'll be using the results of the dataframe from that exercise in this one.)

Complete the function, calc_home_advantage(winners_df), below, so that it returns the top 5 countries, among those that have played at least 50 home games, having the highest home advantage ratio. It should return a dataframe with two columns, team and ratio, holding the name of the team and its home advantage ratio, respectively. The ratio should be rounded to three decimal places. The rows should be sorted in descending order of ratio. If there are two teams with the same winning ratio, the teams should appear in alphabetical order by name.

Note 0. As with our definition of away-games, a team plays a home game if it is the home team (home_team) and the field is non-neutral (i.e., neutral is FALSE).

Note 1. You should find, for example, that Brazil is the number two team, with a home advantage ratio of 0.773.

def calc_home_advantage(winners_df):
    ### BEGIN SOLUTION
    return calc_home_advantage__v1(winners_df)

# Solution method 0 (explicit loop)
def calc_home_advantage__v0(winners_df):
    home_teams = winners_df.home_team.unique()
    final_df = []
    for team in home_teams:
        home_game_df = winners_df[(winners_df.home_team == team) & (winners_df.neutral == 'FALSE')]
        number_of_home_games = home_game_df.shape[0]
        if number_of_home_games < 50:
            continue
        home_team_winners = home_game_df[home_game_df.winner == team]
        num_home_team_wins = home_team_winners.shape[0]
        winning_percentage = round(num_home_team_wins / number_of_home_games, 3)
        data_point = {"team":team, "ratio": winning_percentage}
        final_df.append(data_point)
    final_df = pd.DataFrame(final_df)
    final_df = final_df.sort_values(by = ['ratio', 'team'], ascending = [False, True])
    final_df = final_df[['team', 'ratio']]
    return final_df.iloc[0:5]

# Solution method 1 (no explicit loops)
def calc_home_advantage__v1(winners_df):
    home_games_played = winners_df.groupby('home_team')['home_team'].count() 
    home_teams_50 = home_games_played[home_games_played >= 50] 
    wdf_50 = winners_df.set_index('home_team').loc[home_teams_50.index].reset_index() 
    wdf_50 = wdf_50[wdf_50['neutral'] == 'FALSE']
    wdf_50['home_team_won'] = wdf_50['home_team'] == wdf_50['winner']
    wdf_50_played = wdf_50.groupby('home_team')['home_team'].count()
    wdf_50_won = wdf_50.groupby('home_team')['home_team_won'].sum()
    wdf_50_ratio = (wdf_50_won / wdf_50_played).round(3)
    return wdf_50_ratio.sort_values(ascending=False).head(5).to_frame().reset_index() \
                       .rename(columns={'home_team': 'team', 0: 'ratio'}) \
                       .head(5)
    ### END SOLUTION
# Test: Exercise 4 (exposed)
from IPython.display import display

win_perc = calc_home_advantage(winners_df)

print("The solution, according to you:")
display(win_perc)

df_cols = win_perc.columns.tolist()
df_cols.sort()
desired_cols = ['team', 'ratio']
desired_cols.sort()

assert win_perc.shape[0] == 5, "Expected 5 rows, got {}".format(win_perc.shape[0])
assert win_perc.shape[1] == 2, "Expected 2 columns, got {}".format(win_perc.shape[1])
assert df_cols == desired_cols, "Expected {} columns but got {} columns".format(desired_cols, df_cols)

tolerance = .001
sec_team = win_perc.iloc[1].team
sec_perc = win_perc.iloc[1].ratio

assert (sec_team == "Brazil" and abs(sec_perc - .773) <= tolerance), "Second team should be {} with ratio of {}. \
Got {} with ratio of {}".format("Brazil", .773, sec_team, sec_perc)

print("\n(Passed!)")
The solution, according to you:
team	ratio
0	Spain	0.800
1	Brazil	0.773
2	Iran	0.742
3	Cameroon	0.739
4	Egypt	0.724
(Passed!)
# Hidden test cell: exercise4_hidden

print("""
In addition to the tests above, this cell will include some hidden tests.
You will only know the result when you submit your solution to the
autograder.
""")

### BEGIN HIDDEN TESTS
def sol_4(game_df_sol):
    home_teams = winners_df.home_team.unique()
    final_df = []
    for team in home_teams:
        home_game_df = winners_df[(winners_df.home_team == team) & (winners_df.neutral == 'FALSE')]
        number_of_home_games = home_game_df.shape[0]
        if number_of_home_games < 50:
            continue
        home_team_winners = home_game_df[home_game_df.winner == team]
        num_home_team_wins = home_team_winners.shape[0]
        winning_percentage = round(num_home_team_wins / number_of_home_games, 3)
        data_point = {"team":team, "ratio": winning_percentage}
        final_df.append(data_point)
    
    final_df = pd.DataFrame(final_df)
    final_df = final_df.sort_values(by = ['ratio', 'team'], ascending = [False, True])
    final_df = final_df[['team', 'ratio']]
    return final_df.iloc[0:5]

home_df_sol = sol_4(winners_df)
home_df = calc_home_advantage(winners_df)

home_df_sol = home_df_sol.reset_index(drop=True)
home_df = home_df.reset_index(drop=True)

merged = home_df_sol.merge(home_df, indicator=True, how='outer')
diffs = merged[merged['_merge'] == 'right_only']
assert len(diffs) == 0, "The dataframe doesn't match the expected output on \n{}".format(diffs)
assert home_df.equals(home_df_sol), "The dataframe doesn't match the expected output"

print(home_df)
print("\nPassed!")
### END HIDDEN TESTS
In addition to the tests above, this cell will include some hidden tests.
You will only know the result when you submit your solution to the
autograder.

       team  ratio
0     Spain  0.800
1    Brazil  0.773
2      Iran  0.742
3  Cameroon  0.739
4     Egypt  0.724

Passed!
Exercise 5 (3 points) Now, we've seen how much the home advantage plays in, let us see how the results have looked like in the previous tournaments, for the specific case of the FIFA World Cup matches.

In particular, complete the function, points_table(winners_df, wc_year), below, so that it does the following:

It should take as input a dataframe, winners_df, having a "winner" column like that produced in Exercise 3, as well as a target year, wc_year.
It should consider only games in the given target year. Furthermore, it should only consider games where the tournament column has the value "FIFA World Cup".
It should construct and return a "points table". This table should have two columns, team, containing the team name, and points, containing a points tally has defined below.
To compute the points, give the team 3 points for every win, 1 point for every draw, and 0 points (no points) for a loss.
In case of a tie in the points, sort the teams alphabetically
As an example output, for the 1998 FIFA World Cup, the points table is:

team	points
France	19
Croatia	15
Brazil	13
Netherlands	12
Italy	11
def points_table(winners_df, wc_year):
    ### BEGIN SOLUTION
    return points_table__v1(winners_df, wc_year)

#########################################
# Solution method 0 (explicit loop)

def points_table__v0(winners_df, wc_year):
    world_cup_df = winners_df[winners_df.tournament == 'FIFA World Cup'].copy()
    world_cup_df['year'] = world_cup_df['date'].map(lambda a:extract_year(a))
    world_cup_df = world_cup_df[world_cup_df.year == wc_year]
    wc_teams = set(list(world_cup_df.home_team.unique()) + list(world_cup_df.away_team.unique()))
    points = defaultdict(lambda: 0)
    
    df = []
    for team in wc_teams:
        win_filter = ((world_cup_df.home_team == team) | (world_cup_df.away_team == team)) &\
                    (world_cup_df.winner == team)
        num_wins = world_cup_df[win_filter].shape[0]
        points[team] += num_wins * 3
        
        win_filter = ((world_cup_df.home_team == team) | (world_cup_df.away_team == team)) &\
                    (world_cup_df.winner == "Draw")
        num_draws = world_cup_df[win_filter].shape[0]
        points[team] += num_draws
    
    for key in points.keys():
        df.append({"team": key, "points": points[key]})
    df = pd.DataFrame(df)
    df = df.sort_values(by=["points", "team"], ascending=[False, True])
    df = df[["team", "points"]]
    return df.iloc[0:5]

def extract_year(a):
    return datetime.strptime(a, '%Y-%m-%d').year

#########################################
# Solution method 1 (no explicit loops)

def points_table__v1(winners_df, wc_year):
    wc_df = filter_tournament(filter_year(winners_df, str(wc_year)), 'FIFA World Cup')
    wc_home = get_points_df(wc_df, 'home_team')
    wc_away = get_points_df(wc_df, 'away_team')
    wc_all = wc_home.merge(wc_away, on='team', how='outer').fillna(0)
    wc_all['points'] = (wc_all['points_x'] + wc_all['points_y']).astype(int)
    del wc_all['points_x']
    del wc_all['points_y']
    return wc_all.sort_values(by=['points', 'team'], ascending=[False, True])

def filter_tournament(df, tournament):
    return df[df['tournament'] == tournament]

def get_points_row(row):
    if row.name == row['winner']:
        return 3
    if row['winner'] == 'Draw':
        return 1
    return 0

def get_points_df(df, team):
    df_team = df[[team, 'winner']].rename(columns={team: 'team'}).set_index('team')
    return df_team.apply(get_points_row, axis=1) \
                  .to_frame() \
                  .reset_index() \
                  .rename(columns={0: 'points'}) \
                  .groupby('team').sum() \
                  .reset_index()
### END SOLUTION
# Test: Exercise 5 (exposed)


tbl_1998 = points_table(winners_df, 1998)

assert tbl_1998.iloc[0].team == "France"
assert tbl_1998.iloc[0].points == 19
assert tbl_1998.iloc[1].team == "Croatia"
assert tbl_1998.iloc[1].points == 15
assert tbl_1998.iloc[2].team == "Brazil"
assert tbl_1998.iloc[2].points == 13
assert tbl_1998.iloc[3].team == "Netherlands"
assert tbl_1998.iloc[3].points == 12
assert tbl_1998.iloc[4].team == "Italy"
assert tbl_1998.iloc[4].points == 11

print("\n(Passed!)")
(Passed!)
# Hidden test cell: exercise5_hidden

print("""
In addition to the tests above, this cell will include some hidden tests.
You will only know the result when you submit your solution to the
autograder.
""")

### BEGIN HIDDEN TESTS

tbl_1998 = points_table(winners_df, 1998)

assert tbl_1998.iloc[0].team == "France", "Check your points table for year 1998"
assert tbl_1998.iloc[0].points == 19, "Check your points table for year 1998"
assert tbl_1998.iloc[1].team == "Croatia", "Check your points table for year 1998"
assert tbl_1998.iloc[1].points == 15, "Check your points table for year 1998"
assert tbl_1998.iloc[2].team == "Brazil", "Check your points table for year 1998"
assert tbl_1998.iloc[2].points == 13, "Check your points table for year 1998"
assert tbl_1998.iloc[3].team == "Netherlands", "Check your points table for year 1998"
assert tbl_1998.iloc[3].points == 12, "Check your points table for year 1998"
assert tbl_1998.iloc[4].team == "Italy", "Check your points table for year 1998"
assert tbl_1998.iloc[4].points == 11, "Check your points table for year 1998"

tbl_2002 = points_table(winners_df, 2002)

assert tbl_2002.iloc[0].team == "Brazil", "Check your points table for year 2002"
assert tbl_2002.iloc[0].points == 21, "Check your points table for year 2002"
assert tbl_2002.iloc[1].team == "Germany", "Check your points table for year 2002"
assert tbl_2002.iloc[1].points == 16, "Check your points table for year 2002"
assert tbl_2002.iloc[2].team == "Turkey", "Check your points table for year 2002"
assert tbl_2002.iloc[2].points == 13, "Check your points table for year 2002"
assert tbl_2002.iloc[3].team == "South Korea", "Check your points table for year 2002"
assert tbl_2002.iloc[3].points == 11, "Check your points table for year 2002"
assert tbl_2002.iloc[4].team == "Spain", "Check your points table for year 2002"
assert tbl_2002.iloc[4].points == 11, "Check your points table for year 2002"

tbl_2018 = points_table(winners_df, 2018)

assert tbl_2018.iloc[0].team == "France", "Check your points table for year 2018"
assert tbl_2018.iloc[0].points == 19, "Check your points table for year 2018"
assert tbl_2018.iloc[1].team == "Belgium", "Check your points table for year 2018"
assert tbl_2018.iloc[1].points == 18, "Check your points table for year 2018"
assert tbl_2018.iloc[2].team == "Croatia", "Check your points table for year 2018"
assert tbl_2018.iloc[2].points == 14, "Check your points table for year 2018"
assert tbl_2018.iloc[3].team == "Uruguay", "Check your points table for year 2018"
assert tbl_2018.iloc[3].points == 12, "Check your points table for year 2018"
assert tbl_2018.iloc[4].team == "Brazil", "Check your points table for year 2018"
assert tbl_2018.iloc[4].points == 10, "Check your points table for year 2018"

print("\nPassed!")
### END HIDDEN TESTS
In addition to the tests above, this cell will include some hidden tests.
You will only know the result when you submit your solution to the
autograder.


Passed!
Fin! You’ve reached the end of this part. Don’t forget to restart and run all cells again to make sure it’s all working when run in sequence; and make sure your work passes the submission process. Good luck!
