from threading import Thread
import eyes
import brain
import time

if __name__ == "__main__":
    thread = Thread(target = eyes.loop)
    thread.start()

    time.sleep(5)
    while True:
        eyes.get_instance().setMood(0)
        input('Waiting for user input...')

        eyes.attention(True)
        request = brain.listen()
        eyes.attention(False)
        eyes.get_instance().setCuriosity(True)
        request = brain.translate(request)
        emotion = brain.get_emotion(request)[0]
        intent = brain.get_intent(request)[0]
        eyes.get_instance().setCuriosity(False)
        eyes.attention(False)


        if(emotion["label"] == 'LABEL_3'):
            eyes.get_instance().setMood(2)
        
        if(intent["score"] < 0.8):
            eyes.get_instance().anim_confused()
            eyes.get_instance().setMood(1)
        else:
            eyes.get_instance().anim_laugh()

        print(request)
        print(emotion)
        print(intent)
        time.sleep(2)


    thread.join()
    print("thread finished...exiting")