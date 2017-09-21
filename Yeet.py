import random
from pandas import read_csv, DataFrame
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Reshape
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

    model.add(Dense(64, input_shape=(1,), kernel_initializer='random_uniform',
                bias_initializer='zeros'))
    model.add(Activation('tanh'))
    model.add(Dense(64, input_shape=(3,), kernel_initializer='random_uniform',
                bias_initializer='zeros'))
    model.add(Activation('tanh'))
    model.add(Dense(64, input_shape=(3,), kernel_initializer='random_uniform',
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

def generateSentence(prompts, responses):
    text, count, prompt_id = generatePrompt(prompts)
    respar, resp_id = generateResponse(responses, count)
    print(text.format(*respar))
    textbl = TextBlob(text.format(*respar))
    textblsent = textbl.polarity
    print("Sentiment Analysis : ", str(textblsent))
    return prompt_id, resp_id, textblsent

def rate(prompts, responses):
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
    rating = rating - 1
    return rating

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
    try:
        model.load_weights("weights.hdf5")
    except OSError:
        pass
    except ValueError:
        pass
    print("Cards Against Humanity Generator")
    print("Scale of Hilarity")
    print("1 - Not Funny")
    print("2 - Kind of Funny/Eh")
    print("3 - Funny")
    print("")
    x = DataFrame()
    y = DataFrame()
    for i in range(0,9):
        print("Training item : " + str(i+1))
        prompt_id, resp_id, sent = generateSentence(prompts, responses)
        rating = rate(prompts, responses)
        x[i] = [prompt_id, resp_id, sent]
        y[i] = rating
        print("")
    model.fit(x, y, batch_size=1, epochs=10)
    model.save_weights("weights.hdf5")
    while True:
        new_x = DataFrame()
        new_y = DataFrame()
        print("")
        prompt_id, resp_id, sent = generateSentence(prompts, responses)
        new_x[0] = [prompt_id, resp_id, sent]
        prediction = model.predict(new_x, batch_size=1)
        print("Model Prediction : ")
        prediction = prediction[0]
        print("1 : " + str(prediction[0]))
        print("2 : " + str(prediction[1]))
        print("3 : " + str(prediction[2]))
        rating = rate(prompts, responses)
        new_y.append(rating)
        model.fit(new_x, new_y, batch_size=1, epochs=1)
        model.save_weights("weights.hdf5")


__main__()
