import keras_core as keras


def mlp_builder(input_dim, output_dim):
    activation_function = 'softmax'
    loss = 'categorical_crossentropy'
    if output_dim == 1:
        activation_function = 'sigmoid'
        loss = 'binary_crossentropy'
    print(input_dim, output_dim)

    input_tensor = keras.layers.Input(shape=(input_dim,))
    hl = keras.layers.Dense(128, activation='relu')(input_tensor)
    hl = keras.layers.Dropout(0.1)(hl)
    hl = keras.layers.Dense(64, activation='relu')(hl)
    hl = keras.layers.Dropout(0.1)(hl)
    hl = keras.layers.Dense(34, activation='relu')(hl)
    hl = keras.layers.Flatten()(hl)
    output_tensor = keras.layers.Dense(output_dim, activation=activation_function)(hl)

    model = keras.models.Model(inputs=[input_tensor], outputs=[output_tensor])
    model.compile(optimizer='adam', loss=loss, metrics=['accuracy'])

    return model
