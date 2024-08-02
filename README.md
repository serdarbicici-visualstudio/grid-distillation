# grid-distillation
Further investigation of the clustering distillation of the cat &amp; dog dataset from the [BLG454E-Learning-from-Data](https://github.com/serdarbicici-visualstudio/BLG454E-Learning-from-Data)

## Methodology
The methodology involves applying Principal Component Analysis (PCA) to reduce the dimensionality of the image dataset, transforming the images into a 2D feature space for more efficient processing and visualization. Following PCA, KMeans clustering is performed on the reduced data to group similar images into a predefined number of clusters. In order to ensure a representative and balanced selection of samples from each cluster, a grid-based sampling approach is utilized. This approach divides the 2D PCA-transformed space into a grid and selects samples from each grid cell, maintaining diversity within clusters and across different image classes. 

### Grid Shapes
- **Rectangle**
- **Paralelogram**
- **Triangular**
- **Brick**

<div style="display: flex; justify-content: center;">
    <div style="display: flex; flex-direction: column;">
        <div style="display: flex; justify-content: center;">
            <img src="https://github.com/user-attachments/assets/6c498d53-2c3d-4175-9c93-45f7d638360a" alt="Image 1" style="width: 45%; margin: 5px;">
            <img src="https://github.com/user-attachments/assets/1a098135-591c-4190-bf35-09f290244600" alt="Image 2" style="width: 45%; margin: 5px;">
        </div>
        <div style="display: flex; justify-content: center;">
            <img src="https://github.com/user-attachments/assets/5a779d32-b80f-4077-846f-9d4797c30e79" alt="Image 3" style="width: 45%; margin: 5px;">
            <img src="image4_url](https://github.com/user-attachments/assets/c2b60e92-d153-4988-928c-e06a0a49082d" alt="Image 4" style="width: 45%; margin: 5px;">
        </div>
    </div>
</div>

## Datasets

### Dataset 1 - Digits
- **Description**: 0-9 digits in gray-scale
- **Source**: [scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)
- **Size**: 1800 images (180 each)

### Dataset 2 - Flowers
- **Description**: 5 types of flowers
- **Source**: [Kaggle](https://www.kaggle.com/datasets/kausthubkannan/5-flower-types-classification-dataset)
- **Size**: 5000 images (1000 each)

### Dataset 3 - Gender
- **Description**: male and female faces
- **Source**: [Kaggle](https://www.kaggle.com/datasets/humairmunir/gender-recognizer)
- **Size**: 1292 images (646 each)

## Results
In the benchmark, all methods performed well with only 10% of the original datasets and without perfected models. However, as the number of classes increases, the overall performance of grid-based distillation decreases. The best possible application area of this method is with 2-5 different classes. In that domain, the method yields acceptable results with decreased computing time. In the case of 2 different classes, the method gives more deterministic results over reruns.

## Future Work
A basic Python library will be developed from this methodology by [Serdar Biçici](https://github.com/serdarbicici-visualstudio). 
