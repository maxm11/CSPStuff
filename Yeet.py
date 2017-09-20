import random
from pandas import read_csv
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Reshape
from keras.layers.embeddings import Embedding
from keras.optimizers import SGD
from textblob import TextBlob

def processCAHData():
    try:
        data = read_csv("CAH.csv")
    except FileNotFoundError:
        print("File Not Found")
        exit()
    data.reset_index()
    prompts = data.loc[data['Set'] == 'Prompt']
    responses = data.loc[data['Set'] == 'Response']
    prompts = prompts['Content']
    responses = responses['Content']
    prompts.reset_index()
    responses.reset_index()
    return prompts, responses

def defineModel():
    model = Sequential()

    model.add(Dense(64, input_shape=(2,), kernel_initializer='random_uniform',
                bias_initializer='zeros'))
    model.add(Activation('tanh'))
    model.add(Dense(64, input_shape=(2,), kernel_initializer='random_uniform',
                bias_initializer='zeros'))
    model.add(Activation('tanh'))
    model.add(Dense(64, input_shape=(2,), kernel_initializer='random_uniform',
                bias_initializer='zeros'))
    model.add(Activation('tanh'))
    model.add(Dropout(0, 4))
    model.add(Dense(3, input_shape=(1,)))
    model.add(Activation('tanh'))
    model.add(Dense(3, input_shape=(1,)))
    model.add(Activation('softmax'))
    return model

def generatePrompt(prompts):
    while True:
        while True:
            try:
                prompt = random.choice(prompts)
            except KeyError:
                continue
            break
        prompt_id = int(prompts[prompts == prompt].index[0])
        prompt = prompt.replace("______", "{!s}")
        prompt = prompt.replace("_", "")
        count = prompt.count("{!s}")
        if count == 0:
            count = 1
            prompt = prompt + "{!s}"
            break
        if count == 1:
            break
    return prompt, count, prompt_id

def generateResponse(responses, count):
    resp = []
    for i in range(0, count):
        while True:
            try:
                resp1 = random.choice(responses)
            except KeyError:
                continue
            break

        resp.append(resp1)
    if count == 1:
        resp_id = int(responses[responses == resp1].index[0])
    elif count == 2:
        resp_id = 200000000
        count = 0
        for r in resp:
            count = count + 1
            if count == 1:
                resp_id = resp_id + int(responses[responses == r].index[0]) * 10000
            elif count == 2:
                resp_id = resp_id + int(responses[responses == r].index[0])
    

    return resp, resp_id

def rate(prompts, responses):
    text, count, prompt_id = generatePrompt(prompts)
    respar, resp_id = generateResponse(responses, count)
    print(text.format(*respar))
    textbl = TextBlob(text.format(*respar))
    print("Sentiment Analysis : ", str(textbl.polarity))
    while True:
        try:
            rating = input("Rate this on a scale of 1-3: ")
            rating = int(rating)
        except ValueError:
            print("That was not a number. Try Again")
            continue
        if (rating > 3):
            print("This number is above 3. Try again.")
            continue
        if (rating < 1):
            print("This number is below 0. Try again.")
            continue
        break
    print("")
    rating = rating - 1
    return rating, prompt_id, resp_id

def __main__():
    print("Libraries initialized")
    print("Loading data")
    prompts, responses = processCAHData()
    print("Data loaded")
    print("Defining model")
    model = defineModel()
    print("Compiling model")
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9)
    model.compile(optimizer=sgd, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    print("Cards Against Humanity Generator")
    print("Scale of Hilarity")
    print("1 - Not Funny")
    print("2 - Kind of Funny/Eh")
    print("3 - Funny")
    print("")
    x = []
    y = []
    for i in range(0,9):
        print("Training item : " + str(i+1))
        rating, prompt_id, resp_id = rate(prompts, responses)
        x.append([prompt_id, resp_id])
        y.append(rating)
    print("X:")
    print(x)
    print("Y:")
    print(y)
    model.fit(x, y, batch_size=1, epochs=10)
    while True:
        new_x = []
        new_y = []
        rating, prompt_id, resp_id = rate(prompts, responses)
        new_x.append([prompt_id, resp_id])
        new_y.append(rating)
        prediction = model.predict(x)
        print("Model Prediction : " + str(prediction))
        model.fit(x, y, batch_size=1, epochs=1)


__main__()
