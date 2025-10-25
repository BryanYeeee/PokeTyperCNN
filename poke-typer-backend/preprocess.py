import tensorflow as tf

def preprocess_effnet(image_bytes):
    """Preprocess for EfficientNet models"""
    img = tf.image.decode_image(image_bytes, channels=3)
    img = tf.image.resize(img, (224, 224))
    img = tf.keras.applications.efficientnet.preprocess_input(img)
    return tf.expand_dims(img, axis=0)

def preprocess_resnet(image_bytes):
    """Preprocess for ResNet50 models"""
    img = tf.image.decode_image(image_bytes, channels=3)
    img = tf.image.resize(img, (224, 224))
    img = tf.keras.applications.resnet50.preprocess_input(img)
    return tf.expand_dims(img, axis=0)