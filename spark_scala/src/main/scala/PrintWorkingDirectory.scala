object PrintWorkingDirectory {
  def main(args: Array[String]): Unit = {
    val currentWorkingDirectory = System.getProperty("user.dir")
    println(s"Current working directory: $currentWorkingDirectory")
  }
}