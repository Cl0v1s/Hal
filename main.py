from threading import Thread, Event
import eyes
import bips
import brain
import act
import time

ready = Event()
stop = Event()

NAME = "Merci"

def getCurrentMemoryUsage():
    with open('/proc/self/status') as f:
        memusage = f.read().split('VmRSS:')[1].split('\n')[0]
    return memusage.strip()

if __name__ == "__main__":
    thread = Thread(target = eyes.loop, args=(ready, stop, ))
    thread.start()

    actions = act.load_actions()
    intent_index = dict()
    index = 0
    for action in actions:
        for intent in action[0]:
            intent_index["LABEL_"+ str(index)] = [intent, action[1]]
            index += 1

    while stop.is_set() == False:
        if ready.is_set():
            eyes.get_instance().setMood(0)

            try:

                # Waiting for someone to call Luxie
                brain.wait_for_call(NAME)
                eyes.attention(True)

                # Get a new sample with the actual request
                bips.playListen()
                buffer = brain.listen()

                # Request processing
                request = brain.understand(buffer)
                eyes.attention(False)
                eyes.get_instance().setMood(3)
                eyes.get_instance().setIdleMode(False, 2, 2)
                eyes.get_instance().setCuriosity(True)
                request = brain.translate(request)
                # emotion = brain.get_emotion(request)[0]
                intent = brain.get_intent(request)[0]
                eyes.get_instance().setCuriosity(False)

                # if(emotion["label"] == 'LABEL_3'):
                #     eyes.get_instance().setMood(2)
                
                int, fn = intent_index[intent["label"]]
                if(intent["score"] < 0.80):
                    eyes.get_instance().anim_confused()
                    eyes.get_instance().setMood(1)
                    bips.playSad()
                else:
                    eyes.get_instance().setMood(0)
                    eyes.get_instance().anim_laugh()
                    bips.playOk()
                    fn(int, request)


                time.sleep(0.5)
                eyes.attention(False)
                print(request)
                # print(emotion)
                print(intent)
                print(getCurrentMemoryUsage())
                time.sleep(2)
            except Exception as e:
                print(e)
                bips.playError()
        else: 
            time.sleep(1)

    thread.join()
    print("thread finished...exiting")