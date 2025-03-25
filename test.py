import brain
from word2number import w2n

a = brain.think("What time is mentioned there ?", "What's the weather like at Paris at twelve past three hour ?")
print(a)
print(w2n.word_to_num(a["answer"]))