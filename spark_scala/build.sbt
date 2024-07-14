ThisBuild / version := "0.1.0-SNAPSHOT"
ThisBuild / scalaVersion := "2.13.14"

lazy val root = (project in file("."))
  .settings(
    name := "SparkStreaming",
    resolvers += "Confluent" at "https://packages.confluent.io/maven/",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-core" % "3.3.2",
      "org.apache.spark" %% "spark-streaming" % "3.3.2",
      "org.apache.spark" %% "spark-sql" % "3.3.2",
      "org.apache.hadoop" % "hadoop-client" % "3.3.2",
      "org.java-websocket" % "Java-WebSocket" % "1.5.2",
      "org.json4s" %% "json4s-core" % "3.6.7",
      "org.json4s" %% "json4s-native" % "3.6.7",
      "org.json4s" %% "json4s-jackson" % "3.6.7",
      "org.apache.logging.log4j" % "log4j-core" % "2.14.1",
      "org.apache.logging.log4j" % "log4j-api" % "2.14.1",
      "org.mongodb.spark" %% "mongo-spark-connector" % "10.3.0"
    ),
    mainClass in Compile := Some("Main")
  )
