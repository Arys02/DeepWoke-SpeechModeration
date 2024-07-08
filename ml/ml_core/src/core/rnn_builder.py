import keras_core as keras


def rnn_builder(input_dim, output_dim):
    activation_function = 'softmax'
    loss = 'categorical_crossentropy'
    if output_dim == 1:
        activation_function = 'sigmoid'
        loss = 'binary_crossentropy'
    print(input_dim, output_dim)

    input_dim = input_dim[1]

    input_tensor = keras.layers.Input(shape=(input_dim,))

    hl = keras.layers.SimpleRNN(128)(input_tensor)
    hl = keras.layers.Flatten()(hl)
    output_tensor = keras.layers.Dense(output_dim, activation=activation_function)(hl)

    model = keras.models.Model(inputs=[input_tensor], outputs=[output_tensor])
    model.compile(optimizer='adam', loss=loss, metrics=['accuracy'])

    return model
