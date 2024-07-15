import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions.Window
import scala.util.Random

object Producer {
  def main(args: Array[String]): Unit = {

    // to make the project run on windows you need this folder with winutils.ext and hadoop.dll to be linked
    System.setProperty("hadoop.home.dir", "resources/hadoop")

    val logFile = "source_data/corrected_all_data_with_users_hatespeech_0.csv"

    val spark = SparkSession.builder
      .appName("Producer")
      .master("local[*]")
      .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    val options = Map("delimiter" -> ",", "header" -> "true", "encoding" -> "UTF-8")
    var logData = spark.read.options(options).csv(logFile).persist()

    println("number of lines in my df " + logData.count())
    var partitionIndex = 0

    logData = logData.withColumn("dummy_partition_key", lit(1))
    val windowSpec = Window.partitionBy("dummy_partition_key").orderBy("id")
    logData = logData.withColumn("row_num", row_number().over(windowSpec))

    while (logData.count() > 0) {
      // Determine the size of the current partition randomly between 50 and 100
      val partitionSize = Random.between(500, 1000)
      //val partitionSize = 100

      val toWrite = logData.filter(col("row_num") <= partitionSize)

      println(s"writing to produced_data/partition_${partitionIndex}.csv")
      toWrite.drop("row_num", "dummy_partition_key").write
        .format("csv")
        .options(options + ("encoding" -> "UTF-8"))
        .mode("overwrite")
        .save(s"produced_data/partition_${partitionIndex}")

      // Remove the rows that have been written to the current partition
      logData = logData.filter(col("row_num") > partitionSize)
      println("remain lines in df " + logData.count())

      partitionIndex += 1

      // Optional: Add a delay to simulate real-time partitioning
      //Thread.sleep(10000)

      // Update row numbers after filtering
      logData = logData.withColumn("row_num", row_number().over(windowSpec))
    }
  }
}
