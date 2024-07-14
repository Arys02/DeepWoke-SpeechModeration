import org.apache.spark.sql.{DataFrame, Encoder, Encoders, SparkSession}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.{DoubleType, IntegerType, StringType, StructType}
import org.apache.log4j.{Level, Logger}
import org.java_websocket.client.WebSocketClient
import org.java_websocket.handshake.ServerHandshake
import org.apache.spark.sql.execution.streaming.MemoryStream

import java.net.{HttpURLConnection, URI, URL}
import java.io.{BufferedReader, DataOutputStream, InputStreamReader}
import org.json4s._
import org.json4s.jackson.Serialization
import org.json4s.jackson.Serialization.write
import org.json4s.jackson.JsonMethods._

import java.util.concurrent.{ConcurrentLinkedQueue, Executors, ScheduledExecutorService, TimeUnit}
import scala.collection.mutable
import scala.collection.mutable.Queue
import java.sql.Timestamp
import java.time.Instant

object Consumer {
  implicit val formats: Formats = DefaultFormats

  val scheduler: ScheduledExecutorService = Executors.newScheduledThreadPool(1)

  @volatile var wsClient: WebSocketClient = _
  @volatile var isConnected: Boolean = false

  case class Message(`type`: String, id: String, text: String, user: String, is_hateful: Option[Int])
  case class HateSpeechDetectionResponse(id: String, is_hateful: Int)

  val receivedMessages: ConcurrentLinkedQueue[Message] = new ConcurrentLinkedQueue[Message]()
  implicit val messageEncoder: Encoder[Message] = Encoders.product[Message]

  def main(args: Array[String]): Unit = {

    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)

    def connectToWebSocket(): Unit = {
      wsClient = new WebSocketClient(new URI(s"wss://deepwoke.com/ws?clientType=spark")) {
        override def onOpen(handshakedata: ServerHandshake): Unit = {
          println("WebSocket connection opened")
          isConnected = true
        }

        override def onMessage(message: String): Unit = {
          val receivedMessage = parse(message).extract[Message]
          println(receivedMessage)
          if (receivedMessage.`type` == "inbound") {
            receivedMessages.add(receivedMessage)
          }
        }

        override def onClose(code: Int, reason: String, remote: Boolean): Unit = {
          println(s"WebSocket connection closed: $reason")
          isConnected = false
          scheduleReconnect()
        }

        override def onError(ex: Exception): Unit = {
          println("WebSocket error observed: ")
          ex.printStackTrace()
        }
      }
      wsClient.connect()
    }

    def scheduleReconnect(): Unit = {
      scheduler.schedule(new Runnable {
        override def run(): Unit = {
          connectToWebSocket()
        }
      }, 5, TimeUnit.SECONDS)
    }

    connectToWebSocket()

    val spark = SparkSession.builder()
      .appName("Consumer")
      .master("local[*]")
//      .config("spark.mongodb.input.collection", "messages")
//      .config("spark.mongodb.output.collection", "messages")
      .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1")
      .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    println
    val csvDirectory = "./produced_data"
    //val checkpointLocation = "./checkpoint"

    // Create the checkpoint directory if it does not exist
    //new java.io.File(checkpointLocation).mkdirs()

    val hateSpeechSchema = new StructType()
      .add("type", StringType)
      .add("id", StringType) // Ensure id is String to match the case class
      .add("text", StringType)
      .add("user", StringType)
      .add("is_hateful", IntegerType)

//    val mongoMessageSchema = new StructType()
//      .add("id", DoubleType)
//      .add("is_hateful", IntegerType)
//      .add("text", StringType)
//      .add("user", StringType)


    val csvDF = spark.readStream
      .option("sep", ",")
      .option("header", "true")
      .option("recursiveFileLookup", "true")
      .schema(hateSpeechSchema)
      .csv(csvDirectory)

    val memoryStream = MemoryStream[Message](1, spark.sqlContext)
    val wsDF = memoryStream.toDF()

    // Periodically poll the queue and add messages to the MemoryStream
    new Thread(new Runnable {
      def run(): Unit = {
        while (true) {
          if (!receivedMessages.isEmpty) {
            val messages = new mutable.Queue[Message]()
            while (!receivedMessages.isEmpty) {
              messages += receivedMessages.poll()
            }
            memoryStream.addData(messages)
          }
          //Thread.sleep(1000) // Adjust the sleep time as needed
        }
      }
    }).start()

    val unifiedDF = csvDF.unionByName(wsDF)

    import spark.implicits._

    // Function to call the hate speech detection API
    def detectHateSpeech(messages: Seq[Message]): Seq[HateSpeechDetectionResponse] = {
      val url = new URL("https://deepwoke.com/predict/classify_batch")
      val connection = url.openConnection().asInstanceOf[HttpURLConnection]
      connection.setRequestMethod("POST")
      connection.setRequestProperty("Content-Type", "application/json; charset=UTF-8")
      connection.setDoOutput(true)

      val cleanedMessages = messages.map(msg =>
        msg.copy(text = msg.text.replaceAll("[\\p{Cntrl}&&[^\r\n\t]]", "").replaceAll("\u00A0", " "))
      )
      val jsonString = write(cleanedMessages)

      val outputStream = new DataOutputStream(connection.getOutputStream)
      outputStream.write(jsonString.getBytes("UTF-8"))
      outputStream.flush()
      outputStream.close()

      val responseCode = connection.getResponseCode
      if (responseCode == HttpURLConnection.HTTP_OK) {
        val inputStream = new BufferedReader(new InputStreamReader(connection.getInputStream, "UTF-8"))
        val response = new StringBuffer()
        var inputLine = inputStream.readLine()
        while (inputLine != null) {
          response.append(inputLine)
          inputLine = inputStream.readLine()
        }
        inputStream.close()
        org.json4s.jackson.JsonMethods.parse(response.toString).extract[Seq[HateSpeechDetectionResponse]]
      } else {
        println(connection)
        Seq.empty[HateSpeechDetectionResponse]
      }
    }

    // Variables to store accumulated statistics
    var totalHatefulMessages: Long = 0
    var totalRegularMessages: Long = 0
    var userHatefulCounts: mutable.Map[String, Int] = mutable.Map()
    var wordCounts: mutable.Map[String, Int] = mutable.Map()
    var userTotalCounts: mutable.Map[String, Int] = mutable.Map()

    val query = unifiedDF.writeStream
      .outputMode("append")
      .foreachBatch { (batchDF: DataFrame, batchId: Long) =>
        // Extract messages and call the hate speech detection API
        val messages = batchDF.as[Message].collect().toSeq
        val detectionResults = detectHateSpeech(messages)

        // Update the DataFrame with the hate speech detection results
        val updatedDF = batchDF.as[Message]
          .map { message =>
            detectionResults.find(_.id == message.id) match {
              case Some(detectionResult) => message.copy(is_hateful = Some(detectionResult.is_hateful))
              case None => message
            }
          }
          .toDF()

//        updatedDF.writeStream
//          .format("mongodb")
//          //.option("checkpointLocation", "/tmp/")
//          //.option("forceDeleteTempCheckpointLocation", "true")
//          .option("spark.mongodb.connection.uri", "mongodb://localhost:27017/messages.messages")
//          .option("spark.mongodb.database", "messages")
//          .option("spark.mongodb.collection", "messages")
//          .outputMode("append")

        updatedDF.select("id", "is_hateful", "text", "user")
          .write
          .format("mongodb")
          .mode("append")
          .option("uri", "mongodb://localhost:27017")
          .option("spark.mongodb.database", "messages")
          .option("spark.mongodb.collection", "messages")
          .save()

        // Process updatedDF and update statistics
        totalHatefulMessages += updatedDF.filter(col("is_hateful") === 1).count()
        totalRegularMessages += updatedDF.filter(col("is_hateful") === 0).count()

        // Update user hateful counts
        updatedDF.groupBy("user").agg(
          sum("is_hateful").as("hateful_count"),
          count("id").as("total_count")
        ).collect().foreach(row => {
          val user = row.getString(0)
          val hatefulCount = row.getLong(1).toInt
          val totalCount = row.getLong(2).toInt
          userHatefulCounts(user) = userHatefulCounts.getOrElse(user, 0) + hatefulCount
          userTotalCounts(user) = userTotalCounts.getOrElse(user, 0) + totalCount
        })

        val top5Users = userHatefulCounts.toSeq.sortBy(-_._2).take(5).map { case (user, count) => Map("user" -> user, "count" -> count) }
        val top5UsersByTotal = userTotalCounts.toSeq.sortBy(-_._2).take(5).map { case (user, count) => Map("user" -> user, "count" -> count) }

        val totalMessages = totalHatefulMessages + totalRegularMessages
        val hateSpeechRatio = if (totalMessages > 0) totalHatefulMessages.toDouble / totalMessages else 0.0

        val unwantedWords = Set("je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "le", "la", "les", "un", "une", "des", "sommes", "est",
          "ont", "ai", "are", "c'est", "it's", "is", "was", "by", "en", "sa", "son", "@url", "ne", "not", "pas",
          "that", "a", "n'est", "to", "par", "de", "ce", "sont", "a", "them", "it", "aux", "you", "avec", "in", "dans",
          "@user", "et", "que", "à", "of", "qui", "the", "and", "du", "sur", "si", "if", "au", "aux", "pour", "mais",
          "for", "but", "plus", "suis", "se", "«", "they", "comme", "have", "ou", "?", "quand", "ça", "fait", "c", "tout", "contre")

        updatedDF.select("text").as[String].collect()
          .flatMap(_.split("\\s+"))
          .filterNot(word => unwantedWords.contains(word.toLowerCase))
          .foreach(word => wordCounts(word) = wordCounts.getOrElse(word, 0) + 1)

        val top10Words = wordCounts.toSeq.sortBy(-_._2).take(10).map { case (word, count) => Map("word" -> word, "count" -> count) }

        // Prepare messages to be sent to the WebSocket server
        val messagesToSend = updatedDF.as[Message].collect().toSeq

        val dataToSend = Map(
          "messages" -> messagesToSend,
          "batchSize" -> messagesToSend.size,
          "hatefulBatchSize" -> updatedDF.filter(col("is_hateful") === 1).count(),
          "timestamp" -> Timestamp.from(Instant.now()).toString,
          "totalHatefulMessages" -> totalHatefulMessages,
          "totalRegularMessages" -> totalRegularMessages,
          "totalMessages" -> totalMessages,
          "hateSpeechRatio" -> hateSpeechRatio,
          "top5Users" -> top5Users,
          "top10Words" -> top10Words,
          "top5ActiveUsers" -> top5UsersByTotal
        )

        if (isConnected) {
          try {
            val jsonData = write(dataToSend)
            wsClient.send(jsonData)
            println("sent data")
          } catch {
            case e: Exception => println("Failed to send batch data: " + e.getMessage)
          }
        } else {
          println("WebSocket is not connected. Data not sent.")
        }
      }
      //.option("checkpointLocation", checkpointLocation)
      .start()

    query.awaitTermination()
  }
}
