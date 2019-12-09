import os, sys, pprint, time, json
import config
from parser import Parser

class Trainer:
    def __init__(self, parser):
        self.parser = parser
        self.ds100 = self.parser.load_dictionary(config.DS100)
        self.ds75 = self.parser.load_dictionary(config.DS75)
        self.ds66 = self.parser.load_dictionary(config.DS66)
        self.ds50 = self.parser.load_dictionary(config.DS50)
        self.model = None

    def calculate_model(self, indicators, total_len):
        for ind in indicators:
            for type in indicators[ind]:
                indicators[ind][type] = ((indicators[ind][type] * 100.0) / float(total_len))
        return indicators

    def filter_max(self, indicators):
        for ind in indicators:
            winner = max(indicators[ind], key=indicators[ind].get)
            for type in indicators[ind]:
                if type != winner:
                    indicators[ind][type] = 0
                else:
                    indicators[ind][type] = 1
        return indicators

    def evaluate_words(self, words):
        ind = ''
        expected = 'negative'
        distance = 2
        for wrd in words[ind]:
            for key in words[ind][wrd]:
                if key != expected and words[ind][wrd][key] > words[ind][wrd][expected] + distance:
                    print(ind, wrd, words[ind][wrd])

    def train(self):
        indicators = {}
        words = {}
        total_len = 0

        # configure dataset here
        datasets = [
                     (self.ds100, 100),
                    # (self.ds75, 75),
                    # (self.ds66, 66),
                    # (self.ds50, 50)
                    ]

        for ds_touple in datasets[:1]:
            dataset = ds_touple[0]
            for type in dataset:
                set_len = len(dataset[type])
                total_len += set_len
                for sentence in dataset[type]:
                    result, tokens = self.parser.parse(sentence, require_tokens=True)
                    for ind in result:
                        if ind not in indicators:
                            indicators[ind] = {'positive': 0, 'negative':0, 'neutral': 0}
                        indicators[ind][type] += 1
                    for i in range(0, len(tokens)):
                        if result[i] not in words:
                            words[result[i]] = {}
                        if tokens[i] not in words[result[i]]:
                            words[result[i]][tokens[i]] = {'positive': 0, 'negative':0, 'neutral': 0}
                        words[result[i]][tokens[i]][type] += 1

        print("Total Length: {}".format(total_len))
        self.model = self.calculate_model(indicators, total_len)

        #watchout for this
        self.model['lagging'] = {'positive': 0, 'negative':0, 'neutral': 0}
        self.model['leading'] = {'positive': 0, 'negative':0, 'neutral': 0}
        pprint.pprint(self.model)

        f = open(config.MODEL,'wb')
        json.dump(self.model, f)
        f.close()

        return self.model

    def evaluate(self, model):
        datasets = [
                     (self.ds100, 100),
                     (self.ds75, 75),
                     (self.ds66, 66),
                     (self.ds50, 50)
                    ]
        for_print = []
        for ds_touple in datasets:
            dataset = ds_touple[0]
            total_len = 0
            print("DS: {}".format(ds_touple[1]))
            for type in dataset:
                set_len = len(dataset[type])
                total_len += set_len
                wrong = 0
                sentence_scores = {'positive':0, 'negative':0, 'neutral':0}
                for sentence in dataset[type]:
                    result, tokens = self.parser.parse(sentence, require_tokens=True)
                    if not result:
                        continue
                    score = {'positive':0, 'negative':0, 'neutral':0}
                    for token in result:
                        if token not in model:
                            continue
                        score['positive'] += model[token]['positive']
                        score['negative'] += model[token]['negative']
                        score['neutral'] += model[token]['neutral']
                    if not score['positive'] and not score['negative'] and not score['neutral']:
                        score['neutral'] += 1
                    sentence_scores[max(score, key=score.get)] += 1
                    if max(score, key=score.get) != type:
                        for_print.append({'1': type + " -> " + max(score, key=score.get) + " -> " + sentence, '2': result, '3': tokens, '4':"-"*50})
                        wrong += 1
                print("Accuracy {}: {}".format(type, str(100 - ((wrong * 100)//set_len))))
            print(total_len)
        f = open("for_print", 'wb')
        pprint.pprint(for_print, stream = f)
        f.close()


if __name__ == "__main__":
    parser = Parser()
    trainer = Trainer(parser)
    model = trainer.train()
    trainer.evaluate(model)