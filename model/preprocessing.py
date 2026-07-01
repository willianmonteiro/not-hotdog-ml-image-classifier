"""Image preprocessing for training and evaluation.

Centralizes resize, normalization and augmentation so train.py and evaluate.py
use the exact same pipeline. Reads images directly from the data/ folder structure
and yields batches on the fly.
"""

from pathlib import Path

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# 224x224 matches the input size of common CNNs (VGG/ResNet/MobileNet), which keeps
# transfer learning on the table later.
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
CLASS_MODE = "binary"

MODEL_DIR = Path(__file__).resolve().parent
TRAIN_DIR = MODEL_DIR / "data" / "train"
VALIDATION_DIR = MODEL_DIR / "data" / "validation"


def build_train_generator(data_dir: Path = TRAIN_DIR):
    """Training pipeline: normalization + augmentation.

    Augmentation randomly transforms each image every epoch. With only ~500 images
    this is the main defense against overfitting — the model has to learn what a hotdog
    looks like rather than memorize the training photos.
    """
    datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        zoom_range=0.2,
        horizontal_flip=True,  # no vertical_flip: upside-down food photos don't occur in practice
        fill_mode="nearest",
    )
    return datagen.flow_from_directory(
        data_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode=CLASS_MODE,
        shuffle=True,
    )


def build_validation_generator(data_dir: Path = VALIDATION_DIR):
    """Validation pipeline: normalization only.

    No augmentation, should measure performance on real, untouched images.
    Rescaling stays because the model expects 0–1 inputs.
    """
    datagen = ImageDataGenerator(rescale=1.0 / 255)
    return datagen.flow_from_directory(
        data_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode=CLASS_MODE,
        shuffle=False,  # fixed order keeps the confusion matrix reproducible
    )


def create_data_generators():
    """Return (train_generator, validation_generator)."""
    return build_train_generator(), build_validation_generator()


if __name__ == "__main__":
    train_gen, val_gen = create_data_generators()

    print(f"Class -> index map: {train_gen.class_indices}")
    print(f"Training images:    {train_gen.samples}")
    print(f"Validation images:  {val_gen.samples}")

    images, labels = next(train_gen)
    print(f"Batch shape: {images.shape}, pixel range: [{images.min():.2f}, {images.max():.2f}]")
