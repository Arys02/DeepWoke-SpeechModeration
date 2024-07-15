screen -dmS spark_session bash -c 'echo "runMain Consumer" | sbt > spark_output.log 2>&1'

# Save the screen session name
echo "spark_session" > spark_screen_name.txt

echo "Spark job started."