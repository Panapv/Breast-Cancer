# Breast Cancer Prediction Model

## Overview
This repository contains code and resources for a predictive model that determines whether a breast tumor is benign or malignant. The model is built using machine learning techniques on the Breast Cancer Wisconsin (Diagnostic) Dataset from Kaggle.

## Dataset
The dataset used for this project is the Breast Cancer Wisconsin (Diagnostic) Dataset from Kaggle. It includes features computed from digitized images of breast mass and aims to classify tumors into benign and malignant categories based on these features.

## Project Structure
- **data/**: Directory containing the dataset files divided into raw, staging, and business.
- **docs/**: Contains the files required for Sphinx to work.
- **model/**:
  - `Jupyter notebook`: Used for data exploration, preprocessing, model development, and evaluation. Contains the report about the models.
  - **models/**: Saved models after training.
- **test/**: Unit tests of classes and data quality.
- **requirements.txt**: List of Python dependencies for reproducing the environment.
- **Handler.py**: Contains all the functions required for the ETL data flow.
- **S3Client.py**: Contains all the features required for bucket creation and connection to AWS.

## Methodology
- **Data Preprocessing**: We use Kaggle for data and PySpark for transformation, leveraging its distributed processing power. We then upload the processed data to an AWS bucket, ensuring secure and accessible storage.
- **Model Development**: Implemented a machine learning pipeline using scikit-learn to train and validate several classification models:
  - Random Forest Classifier
  - Random Forest Classifier with hyperparameter search engine
  - Neuronal Network
- **Model Evaluation**: Evaluated models using metrics such as accuracy, precision, recall, and F1-score. Cross-validation and hyperparameter tuning were performed to optimize model performance.

## Usage
To run the notebooks and scripts in this repository, follow these steps:
1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/Breast-Cancer.git
   cd Breast-Cancer

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. The `kaggle.json` file must be placed in a folder named `.kaggle` in your home directory.<br>Ensure that the `kaggle.json` file correctly contains your Kaggle API credentials.<br>If this folder does not exist, you must create it manually. The full path should be `~/.kaggle/kaggle.json`.

- On Unix/Linux and macOS systems, `~` represents your home directory. You can navigate to this location using the command `cd ~` in the terminal.
- On Windows, the equivalent directory would be `C:\Users\your_username\.kaggle\`.

4. Create a .env with the following structure and your own tokens:
   ```bash
   AWS_ACCESS_KEY_ID = ''
   AWS_SECRET_ACCESS_KEY = ''
   
5. Navigate to the **main.py** script and execute it.<br>
Then access the **model/** directory to open the Jupyter Notebook with the transformed data and proceed with the analysis, model training, and evaluation.<br>
Execute the notebook in sequential order to reproduce the analysis, model training, and evaluation.

## Results

The best performing model (Neuronal Network) achieved an accuracy of 98% on the test set, demonstrating effective prediction of benign and malignant tumors based on the provided features.

## Future Work

Future improvements could include:
- Exploring deep learning models for potential performance gains.
- Integrating additional medical data or features for enhanced predictive power.
- Deploying the model as a web application or API for real-time predictions.

## Contributors

- [Pablo Pérez Vázquez](https://github.com/Panapv)
- [Pedro Mera Piñeiro](https://github.com/merpinped)
- [Vanesa Blanco Cruz](https://github.com/blacruvan)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Kaggle for providing the Breast Cancer Wisconsin (Diagnostic) Dataset.
- Open-source contributors whose libraries and tools facilitated this project.
