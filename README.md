# DeepWoke

## Project Overview

DeepWoke is a comprehensive project designed for online moderation. It leverages advanced machine learning models and real-time data processing to detect and manage inappropriate content across various platforms. The project is divided into several key components, each serving a specific function in the overall system.

## Repository Structure

This repository contains the following main directories:

```
- ./
  - bot_discord/
  - ml/
    - fast_api_model/
      - tests/
    - ml_core/
      - data/
        - embedding_data/
        - external/
        - processed/
        - raw/
      - docs/
      - embedded_vector/
      - log/
        - fit/
      - model_weights/
      - notebooks/
        - data/
        - embedding/
        - model/
      - src/
        - core/
        - data/
        - embedding/
      - tests/
  - out/
  - spark_scala/
    - project/
    - resources/
      - hadoop/
        - bin/
    - source_data/
    - src/
      - main/
        - scala/
  - spark_streaming_dashboard/
    - public/
    - src/
      - api/
      - components/
      - hooks/
      - models/
      - pages/
      - styles/
      - test/
```

## Components Description

### Bot Discord
The `bot_discord` directory contains the source code for the Discord bot. This bot monitors and moderates conversations in real-time to detect inappropriate content.

### Machine Learning (ml)
The `ml` directory is divided into two main parts:

- **fast_api_model**: This contains the API developed in Python for serving machine learning models. It includes a `tests` directory for unit and integration tests.
  
- **ml_core**: This includes the core machine learning components:
  - `data`: Contains subdirectories for different stages of data (embedding_data, external, processed, raw).
  - `docs`: Documentation for the machine learning models and processes.
  - `embedded_vector`: Stores embedded vectors used by the models.
  - `log`: Contains logs, with a subdirectory `fit` for model fitting logs.
  - `model_weights`: Stores the trained model weights.
  - `notebooks`: Jupyter notebooks for data analysis and model training, categorized into data, embedding, and model.
  - `src`: Source code for core functionalities, data processing, and embedding generation.
  - `tests`: Contains test scripts for validating the machine learning components.

### Spark Scala
The `spark_scala` directory includes the code for the Spark Streaming application developed in Scala:
- `project`: Configuration and setup files for the Scala project.
- `resources`: Contains resources needed by the application, including Hadoop binaries.
- `source_data`: Source data for the Spark application.
- `src`: Main source code, organized under the `main/scala` directory.

### Spark Streaming Dashboard
The `spark_streaming_dashboard` directory contains the code for the dashboard developed in React:
- `public`: Static assets and public files.
- `src`: Source code organized into various parts such as api, components, hooks, models, pages, styles, and test.

## Getting Started

To get started with the DeepWoke project, follow these steps:

1. **Clone the repository**:
   ```
   git clone <repository_url>
   cd DeepWoke
   ```

2. **Setup Bot Discord**:
   Navigate to the `bot_discord` directory and follow the setup instructions in the README file.

3. **Setup Machine Learning API**:
   Navigate to the `ml/fast_api_model` directory. Install the required dependencies and run the API.

4. **Setup Spark Scala Application**:
   Navigate to the `spark_scala` directory. Build and run the Scala application following the instructions provided.

5. **Setup Spark Streaming Dashboard**:
   Navigate to the `spark_streaming_dashboard` directory. Install the dependencies and start the React application.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Make sure to follow the coding standards and include appropriate tests.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

This README provides a comprehensive overview of the DeepWoke project, its structure, and how to get started. If you need further customization or additional sections, feel free to ask!