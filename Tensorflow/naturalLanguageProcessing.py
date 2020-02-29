import tensorflow as tf
import tensorflow_datasets as tfds

BUFFER_SIZE = 10000
BATCH_SIZE = 64  # for training

class NLP:

    def __init__(self):
        self.dataSet, self.info = tfds.load('imdb_reviews/subwords8k', with_info=True, as_supervised=True)
        self.train_dataSet = self.dataSet['train']
        self.test_dataSet = self.dataSet['test']
        self.encoder = self.info.features['text'].encoder
        self.model = self.create_model()

    def create_model(self):
        padded_shapes = ([None], ())
        self.train_dataSet = self.train_dataSet.shuffle(BUFFER_SIZE).padded_batch(BATCH_SIZE, padded_shapes=padded_shapes)
        self.test_dataSet = self.test_dataSet.padded_batch(BATCH_SIZE, padded_shapes=padded_shapes)

        model = tf.keras.Sequential([tf.keras.layers.Embedding(self.encoder.vocab_size, 64),
                                     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
                                     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
                                     tf.keras.layers.Dense(64, activation='relu'),
                                     tf.keras.layers.Dropout(0.5),
                                     tf.keras.layers.Dense(1, activation='sigmoid')])

        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                      optimizer=tf.keras.optimizers.Adam(1e-4),
                      metrics=['accuracy'])

        history = model.fit(self.train_dataSet, epochs=5, validation_data=self.test_dataSet, validation_steps=30)
        return model

    # pad the vectors
    def pad_to_size(self, vec, size):
        zeros = [0] * (size - len(vec))
        vec.extend(zeros)
        return vec

    # generate a prediction
    def predict(self, post, pad):
        encoded_sample_pred_text = self.encoder.encode(post)
        if pad:
            encoded_sample_pred_text = self.pad_to_size(encoded_sample_pred_text, 64)
        encoded_sample_pred_text = tf.cast(encoded_sample_pred_text, tf.float32)
        predictions = self.model.predict(tf.expand_dims(encoded_sample_pred_text, 0))
        return predictions

    def test_run(self):
        sample_text = ('This movie was awesome. The acting was incredible.')
        prediction_ex = self.predict(sample_text, pad=True) * 100

        print('Probability this is a positive %.2f' % prediction_ex)

        sample_text2 = ('This movie was so so. The acting was medicore.')
        prediction_ex2 = self.predict(sample_text2, pad=True) * 100

        print('(2) Probability this is a positive %.2f' % prediction_ex2)

    def twitter_posts_trend_analyze(self):
        pass
