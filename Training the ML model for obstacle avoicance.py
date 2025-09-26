from google.colab import drive
drive.mount('/content/drive')

pip install everywhereml>=0.2.19
from logging import basicConfig, INFO
from everywhereml.data import ImageDataset

# Configure basic logging
basicConfig(level=INFO)

# Define the paths to the directories containing images for the four labels
label_paths = {
    'leftturn': '/content/drive/MyDrive/data for google colab/image data for hog  feature test/leftturn',
    'rightturn': '/content/drive/MyDrive/data for google colab/image data for hog  feature test/rightturn',
    'straight': '/content/drive/MyDrive/data for google colab/image data for hog  feature test/straight'
}

# Load the images and store them in the ImageDataset class
try:
    image_dataset = ImageDataset.from_nested_folders(name='Dataset', base_folder='/content/drive/MyDrive/data for google colab/image data for hog  feature test')
except FileNotFoundError:
    image_dataset = ImageDataset.from_nested_folders(name='Dataset', base_folder='/content/drive/MyDrive/data for google colab/image data for hog  feature test', label_paths=label_paths)

# Print the resulting ImageDataset
print(image_dataset)

image_dataset.preview(
    samples_per_class=10,
    rows_per_class=2,
    figsize=(20, 10),
    cmap='gray'
)

from everywhereml.preprocessing.image.transform import Resize
image_dataset = image_dataset.gray().uint8()

"""
Preview grayscale images
"""
image_dataset.preview(
    samples_per_class=10,
    rows_per_class=2,
    figsize=(20, 10),
    cmap='gray'
)

"""
Create an image recognition pipeline with HOG feature extractor
"""
from everywhereml.preprocessing.image.object_detection import HogPipeline
from everywhereml.preprocessing.image.transform import Resize
pipeline = HogPipeline(
    transforms=[
        Resize(width=40, height=30)
    ]
)

# Convert images to feature vectors
feature_dataset = pipeline.fit_transform(image_dataset)
feature_dataset.describe()

"""
Print pipeline description
"""
print(pipeline)

"""
Create and fit RandomForest classifier
"""
from everywhereml.sklearn.ensemble import RandomForestClassifier

for i in range(10):
    clf = RandomForestClassifier(n_estimators=5, max_depth=10)

    # fit on train split and get accuracy on the test split
    train, test = feature_dataset.split(test_size=0.4, random_state=i)
    clf.fit(train)

    print('Score on test set: %.2f' % clf.score(test))

# now fit on the whole dataset
clf.fit(feature_dataset)

"""
Export pipeline to C++
"""
print(pipeline.to_arduino_file(
    filename='C:/Users/Yuto/Desktop/HogPipeline.h',
    instance_name='hog'
))

"""
Export classifier to C++
"""
print(clf.to_arduino_file(
    filename='C:/Users/Yuto/Desktop/HogPipeline.h',
    instance_name='classifier',
    class_map=feature_dataset.class_map
))