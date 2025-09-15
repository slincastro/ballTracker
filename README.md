# Ball Tracker

A project for tracking and predicting ball trajectories using computer vision and deep learning techniques.

## Files

### creating_dataset.py
A Python script that uses a Raspberry Pi camera to capture sequences of images. It takes multiple photos at specified intervals, organizing them into unique UUID-named directories. This script is used to create the raw dataset of ball trajectory images for training and testing the models.

### cnn-gru.ipynb
A Jupyter notebook that implements a hybrid CNN-GRU neural network model for ball trajectory prediction. The CNN component processes image frames, while the GRU component handles the temporal sequence data. The notebook includes data loading, model definition, training, and visualization of results.

### gru.ipynb
A Jupyter notebook that implements a GRU (Gated Recurrent Unit) neural network for predicting ball trajectories based on position data rather than images. It includes data preprocessing, feature engineering, model definition, training, and evaluation with various metrics like Average Displacement Error (ADE) and Final Displacement Error (FDE).

### Utilitarios.ipynb
A utility notebook containing various helper functions for image processing, including image binarization to isolate the ball from the background, image mirroring to augment the dataset, directory renaming utilities, and functions to count available trajectory sequences.

### settings_tester.py
A script for testing and optimizing Raspberry Pi camera settings. It systematically varies parameters like exposure time, gain, saturation, and contrast, capturing images with each configuration to determine the optimal settings for ball tracking.

### .gitignore
A configuration file for Git that specifies which files and directories should be ignored in version control.

## Directories

### fotos_binarizadas_limpias
Contains the processed binary images of ball trajectories. These are cleaned and binarized versions of the original images, where the ball has been isolated from the background. Each subdirectory represents a unique trajectory sequence.

### lightning_logs
Contains training logs and model checkpoints generated during the training of the neural network models using PyTorch Lightning.

### processed
Contains processed data files used for model training and evaluation.
