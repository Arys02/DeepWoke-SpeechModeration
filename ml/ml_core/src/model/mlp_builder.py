import keras_core as keras


def mlp_builder(input_dim, output_dim):
    input_tensor = keras.layers.Input(shape=(input_dim,))
    hl = keras.layers.Dense(128, activation='relu')(input_tensor)
    #hl = keras.layers.Dropout(0.1)(hl)
    hl = keras.layers.Dense(64, activation='relu')(hl)
    #hl = keras.layers.Dropout(0.1)(hl)
    hl = keras.layers.Dense(34, activation='relu')(hl)
    hl = keras.layers.Flatten()(hl)
    output_tensor = keras.layers.Dense(output_dim, activation=keras.activations.softmax)(hl)

    model = keras.models.Model(inputs=[input_tensor], outputs=[output_tensor])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model
