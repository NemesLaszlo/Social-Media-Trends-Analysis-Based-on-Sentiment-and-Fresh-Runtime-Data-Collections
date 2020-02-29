import tensorflow as tf
import tensorflow_datasets as tfds

BUFFER_SIZE = 10000
BATCH_SIZE = 64  # for training

dataSet, info = tfds.load('imdb_reviews/subwords8k', with_info=True, as_supervised=True)
train_dataSet, test_dataSet = dataSet['train'], dataSet['test']
encoder = info.features['text'].encoder

padded_shapes = ([None], ())
train_dataSet = train_dataSet.shuffle(BUFFER_SIZE).padded_batch(BATCH_SIZE, padded_shapes=padded_shapes)
test_dataSet = test_dataSet.padded_batch(BATCH_SIZE, padded_shapes=padded_shapes)

model = tf.keras.Sequential([tf.keras.layers.Embedding(encoder.vocab_size, 64),
                             tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
                             tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
                             tf.keras.layers.Dense(64, activation='relu'),
                             tf.keras.layers.Dropout(0.5),
                             tf.keras.layers.Dense(1, activation='sigmoid')])

model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

history = model.fit(train_dataSet, epochs=5, validation_data=test_dataSet, validation_steps=30)


# pad the vectors
def pad_to_size(vec, size):
    zeros = [0] * (size - len(vec))
    vec.extend(zeros)
    return vec


# generate a prediction
def predict(post, pad):
    encoded_sample_pred_text = encoder.encode(post)
    if pad:
        encoded_sample_pred_text = pad_to_size(encoded_sample_pred_text, 64)
    encoded_sample_pred_text = tf.cast(encoded_sample_pred_text, tf.float32)
    predictions = model.predict(tf.expand_dims(encoded_sample_pred_text, 0))
    return predictions

sample_text = ('This movie was awesome. The acting was incredible.')
prediction_ex = predict(sample_text, pad=True) * 100

print('Probability this is a positive %.2f' % prediction_ex)

sample_text = ('This movie was so so. The acting was medicore.')
prediction_ex = predict(sample_text, pad=True) * 100

print('(2) Probability this is a positive %.2f' % prediction_ex)

