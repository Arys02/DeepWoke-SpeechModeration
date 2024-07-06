import keras_core as keras


def convnet_builder(input_dim, output_dim):
    activation_function = 'softmax'
    loss = 'categorical_crossentropy'
    if output_dim == 1:
        activation_function = 'sigmoid'
        loss = 'binary_crossentropy'
    print(input_dim, output_dim)

    inputs = input_dim[1:]

    input_tensor = keras.layers.Input(shape=inputs)
    layer = keras.layers.Conv1D(32, 1, activation='relu')(input_tensor)
    layer = keras.layers.Conv1D(32, 1, activation='relu')(layer)
    layer = keras.layers.Dropout(0.3)(layer)
    layer = keras.layers.MaxPooling1D(pool_size=1)(layer)

    layer = keras.layers.Conv1D(62, 1, activation='relu')(layer)
    layer = keras.layers.Conv1D(62, 1, activation='relu')(layer)
    layer = keras.layers.Dropout(0.3)(layer)
    layer = keras.layers.MaxPooling1D(pool_size=1)(layer)

    layer = keras.layers.Conv1D(128, 1, activation='relu')(layer)
    layer = keras.layers.Conv1D(128, 1, activation='relu')(layer)
    layer = keras.layers.Dropout(0.3)(layer)
    layer = keras.layers.MaxPooling1D(pool_size=1)(layer)
    layer = keras.layers.Flatten()(layer)

    output_tensor = keras.layers.Dense(output_dim, activation=activation_function)(layer)

    model = keras.models.Model(inputs=[input_tensor], outputs=[output_tensor])
    model.compile(optimizer='adam', loss=loss, metrics=['accuracy'])

    return model
