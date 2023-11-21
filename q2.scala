// Databricks notebook source
// STARTER CODE - DO NOT EDIT THIS CELL
import org.apache.spark.sql.functions.desc
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import spark.implicits._
import org.apache.spark.sql.expressions.Window

// COMMAND ----------

// STARTER CODE - DO NOT EDIT THIS CELL
spark.conf.set("spark.sql.legacy.timeParserPolicy","LEGACY")

// COMMAND ----------

// STARTER CODE - DO NOT EDIT THIS CELL
val customSchema = StructType(Array(StructField("lpep_pickup_datetime", StringType, true), StructField("lpep_dropoff_datetime", StringType, true), StructField("PULocationID", IntegerType, true), StructField("DOLocationID", IntegerType, true), StructField("passenger_count", IntegerType, true), StructField("trip_distance", FloatType, true), StructField("fare_amount", FloatType, true), StructField("payment_type", IntegerType, true)))

// COMMAND ----------

// STARTER CODE - YOU CAN LOAD ANY FILE WITH A SIMILAR SYNTAX.
val df = spark.read
   .format("com.databricks.spark.csv")
   .option("header", "true") // Use first line of all files as header
   .option("nullValue", "null")
   .schema(customSchema)
   .load("/FileStore/tables/nyc_tripdata.csv") // the csv file which you want to work with
   .withColumn("pickup_datetime", from_unixtime(unix_timestamp(col("lpep_pickup_datetime"), "MM/dd/yyyy HH:mm")))
   .withColumn("dropoff_datetime", from_unixtime(unix_timestamp(col("lpep_dropoff_datetime"), "MM/dd/yyyy HH:mm")))
   .drop($"lpep_pickup_datetime")
   .drop($"lpep_dropoff_datetime")

// COMMAND ----------

// LOAD THE "taxi_zone_lookup.csv" FILE SIMILARLY AS ABOVE. CAST ANY COLUMN TO APPROPRIATE DATA TYPE IF NECESSARY.
val df1 = spark.read
    .format("com.databricks.spark.csv")
    .option("header", "true") // Use first line of all files as header
    .option("nullValue", "null")
    .option("inferSchema",true)
    .load("/FileStore/tables/taxi_zone_lookup.csv") 

// ENTER THE CODE BELOW

// COMMAND ----------

// STARTER CODE - DO NOT EDIT THIS CELL
// Some commands that you can use to see your dataframes and results of the operations. You can comment the df.show(5) and uncomment display(df) to see the data differently. You will find these two functions useful in reporting your results.
// display(df)
df.show(5) // view the first 5 rows of the dataframe

// COMMAND ----------

// STARTER CODE - DO NOT EDIT THIS CELL
// Filter the data to only keep the rows where "PULocationID" and the "DOLocationID" are different and the "trip_distance" is strictly greater than 2.0 (>2.0).

// VERY VERY IMPORTANT: ALL THE SUBSEQUENT OPERATIONS MUST BE PERFORMED ON THIS FILTERED DATA

val df_filter = df.filter($"PULocationID" =!= $"DOLocationID" && $"trip_distance" > 2.0)
df_filter.show(5)

// COMMAND ----------

// PART 1a: List the top-5 most popular locations for dropoff based on "DOLocationID", sorted in descending order by popularity. If there is a tie, then the one with the lower "DOLocationID" gets listed first

// Output Schema: DOLocationID int, number_of_dropoffs int 

// Hint: Checkout the groupBy(), orderBy() and count() functions.

// ENTER THE CODE BELOW
val df_pop_dol = df_filter
  .groupBy("DOLocationID")
  .agg(count("*").as("number_of_dropoffs"))
  .orderBy(col("number_of_dropoffs").desc, col("DOLocationID").asc)
  .limit(5)

df_pop_dol.show(5)


// COMMAND ----------

// PART 1b: List the top-5 most popular locations for pickup based on "PULocationID", sorted in descending order by popularity. If there is a tie, then the one with the lower "PULocationID" gets listed first.
 
// Output Schema: PULocationID int, number_of_pickups int

// Hint: Code is very similar to part 1a above.

// ENTER THE CODE BELOW
val df_pop_pul = df_filter
  .groupBy("PULocationID")
  .agg(count("*").as("number_of_pickups"))
  .orderBy(col("number_of_pickups").desc, col("PULocationID").asc)
  .limit(5)

df_pop_pul.show(5)


// COMMAND ----------

// PART 2: List the top-3 locationID’s with the maximum overall activity. Here, overall activity at a LocationID is simply the sum of all pickups and all dropoffs at that LocationID. In case of a tie, the lower LocationID gets listed first.

//Note: If a taxi picked up 3 passengers at once, we count it as 1 pickup and not 3 pickups.

// Output Schema: LocationID int, number_activities int

// Hint: In order to get the result, you may need to perform a join operation between the two dataframes that you created in earlier parts (to come up with the sum of the number of pickups and dropoffs on each location). 

// ENTER THE CODE BELOW
val part2 = df_pop_pul
  .join(
    df_pop_dol,
    df_pop_pul("PULocationID").cast(IntegerType) === df_pop_dol("DOLocationID").cast(IntegerType)
  )
  .select(
    col("PULocationID").as("LocationID"),
    (col("number_of_pickups") + col("number_of_dropoffs")).as("number_activities")
  )
  .orderBy(col("number_activities").desc, col("LocationID").asc)

part2.show(3)


// COMMAND ----------

// PART 3: List all the boroughs (of NYC: Manhattan, Brooklyn, Queens, Staten Island, Bronx along with "Unknown" and "EWR") and their total number of activities, in descending order of total number of activities. Here, the total number of activities for a borough (e.g., Queens) is the sum of the overall activities (as defined in part 2) of all the LocationIDs that fall in that borough (Queens). 

// Output Schema: Borough string, total_number_activities int

// Hint: You can use the dataframe obtained from the previous part, and will need to do the join with the 'taxi_zone_lookup' dataframe. Also, checkout the "agg" function applied to a grouped dataframe.

// ENTER THE CODE BELOW
part2
  .join(
    df1,
    df1("LocationID").cast(IntegerType) === part2("LocationID").cast(IntegerType)
  )
  .select(
    col("Borough"),
    col("number_activities")
  )
  .groupBy("Borough")
  .agg(sum(col("number_activities")).as("total_number_activities"))
  .orderBy(col("total_number_activities").desc)
  .show()


// COMMAND ----------

// PART 4: List the top 2 days of week with the largest number of daily average pickups, along with the average number of pickups on each of the 2 days in descending order (no rounding off required). Here, the average pickup is calculated by taking an average of the number of pick-ups on different dates falling on the same day of the week. For example, 02/01/2021, 02/08/2021 and 02/15/2021 are all Mondays, so the average pick-ups for these is the sum of the pickups on each date divided by 3.

//Note: The day of week is a string of the day’s full spelling, e.g., "Monday" instead of the		number 1 or "Mon". Also, the pickup_datetime is in the format: yyyy-mm-dd.

// Output Schema: day_of_week string, avg_count float

// Hint: You may need to group by the "date" (without time stamp - time in the day) first. Checkout "to_date" function.

// ENTER THE CODE BELOW
df_filter
  .groupBy(to_date(col("pickup_datetime"), "yyyy-MM-dd").as("date"))
  .agg(count("*").as("total_count"))
  .select(date_format(col("date"), "EEEE").as("day_of_week"), col("total_count"))
  .groupBy(col("day_of_week"))
  .agg(avg("total_count").as("avg_count"))
  .orderBy(col("avg_count").desc)
  .limit(2)
  .show()


// COMMAND ----------

// PART 5: For each hour of a day (0 to 23, 0 being midnight) - in the order from 0 to 23(inclusively), find the zone in the Brooklyn borough with the LARGEST number of total pickups. 

//Note: All dates for each hour should be included.

// Output Schema: hour_of_day int, zone string, max_count int

// Hint: You may need to use "Window" over hour of day, along with "group by" to find the MAXIMUM count of pickups

// ENTER THE CODE BELOW
// Extract the hour from pickup_datetime
df_filter
  .withColumn("hour", hour(col("pickup_datetime").cast(TimestampType)))
  .show()

// Define a window specification for ordering by "count" in descending order
val windowSpec = Window.partitionBy("hour").orderBy(col("count").desc)

// Join df_filter with df1, filter for "Brooklyn" Borough, and calculate the max count per hour per Zone
df_filter
  .join(df1, df1("LocationID").cast(IntegerType) === df_filter("PULocationID").cast(IntegerType))
  .filter(col("Borough") === "Brooklyn")
  .select(col("Zone"), col("pickup_datetime"))
  .withColumn("hour", hour(col("pickup_datetime").cast(TimestampType)))
  .groupBy(col("Zone"), col("hour"))
  .agg(count("*").as("count"))
  .withColumn("row_number", row_number.over(windowSpec))
  .filter(col("row_number") === 1)
  .select(col("hour").as("hour_of_day"), col("Zone"), col("count").as("max_count"))
  .show(25, false)

// Group by "Borough" and calculate the total number of activities, then order by total number of activities in descending order
df_filter
  .groupBy("Borough")
  .agg(sum(col("number_activities")).as("total_number_activities"))
  .orderBy(col("total_number_activities").desc)
  .show()



// COMMAND ----------

// PART 6 - Find which 3 different days in the month of January, in Manhattan, saw the largest positive percentage increase in pick-ups compared to the previous day, in the order from largest percentage increase to smallest percentage increase 

// Note: All years need to be aggregated to calculate the pickups for a specific day of January. The change from Dec 31 to Jan 1 can be excluded.

// Output Schema: day int, percent_change float


// Hint: You might need to use lag function, over a window ordered by day of month.

// ENTER THE CODE BELOW
val windowSpec = Window.partitionBy().orderBy(col("day").asc)

df_filter
  .join(df1, df1("LocationID").cast(IntegerType) === df_filter("PULocationID").cast(IntegerType))
  .filter(col("Borough") === "Manhattan" && (date_format(col("pickup_datetime"), "M").cast(IntegerType)) === '2')
  .withColumn("month", date_format(col("pickup_datetime"), "M").cast(IntegerType))
  .show(100)

df_filter
  .join(df1, df1("LocationID").cast(IntegerType) === df_filter("PULocationID").cast(IntegerType))
  .filter(col("Borough") === "Manhattan" && (date_format(col("pickup_datetime"), "M").cast(IntegerType) === '1'))
  .withColumn("day", date_format(col("pickup_datetime"), "d").cast(IntegerType))
  .groupBy(col("day"))
  .agg(count("*").as("pickup_count"))
  .withColumn("prev_pickup_count", lag(col("pickup_count"), 1, 0.0).over(windowSpec))
  .orderBy(col("day").asc)
  .select(col("day"), round((lit(100) * ((col("pickup_count") - col("prev_pickup_count")) / col("prev_pickup_count"))), 2).as("percent_change"))
  .orderBy(col("percent_change").desc)
  .show(3)

