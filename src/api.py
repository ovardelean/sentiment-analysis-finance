import os, sys
import nltk

import config
import parser


class SentimentAPI(object):
    def __init__(self):
        self.parser = parser.Parser()
        self.model = self.parser.load_dictionary(config.MODEL)

    def sentiment(self, text):
        sentences = nltk.sent_tokenize(text)
        total_scores = {'positive':0, 'negative':0, 'neutral':0}
        nr_sentences = len(sentences)
        for sent in sentences:
            results = self.parser.parse(sent)
            score = {'positive':0, 'negative':0, 'neutral':0}
            for token in results:
                score['positive'] += self.model[token]['positive']
                score['negative'] += self.model[token]['negative']
                score['neutral'] += self.model[token]['neutral']
            if not score['positive'] and not score['negative'] and not score['neutral']:
                score['neutral'] += 1
            total_scores[max(score, key=score.get)] += 1
        return {'positive': total_scores['positive'] / float(nr_sentences),
                'neutral': total_scores['neutral'] / float(nr_sentences),
                'negative': total_scores['negative'] / float(nr_sentences)}

def main():
    api = SentimentAPI()
    text_file = sys.argv[1]
    fdata = open(text_file, 'rb').read()
    verdict = api.sentiment(fdata)
    print verdict

if __name__ == "__main__":
    main()
