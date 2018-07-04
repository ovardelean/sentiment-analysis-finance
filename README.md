Sentiment Analysis for Financial Text

Method Proposed: 
	Mining-based hierarchical classifier using Performance Indicators along with positive and negative dictionaries

Dictionaries structure:
	Lagging words: divident, cash, earnings, net sale, revenue, etc.
	Lagging-rev words: cost, expenses, net loss, taxes, operating cost, etc.
	Leading: capacity, contract, employee, offering, personnel, production, etc.
	Directionality: boost, double, climb, decrease, fall, jump, etc
	Positive: good, better, best, boom, brilliant, etc.
	Negative: bad, accused, crisis, cutbacks, damage, etc.

Model performance on datasets:
	DS: 100 (100% agreement) - Length: 2264
		Accuracy positive: 93%
		Accuracy neutral: 90%
		Accuracy negative: 81%
	DS: 75 (75% agreement) - Length 3453
		Accuracy positive: 89%
		Accuracy neutral: 85%
		Accuracy negative: 77%
	DS: 66 (66% agreement) - Length 4217
		Accuracy positive: 87%
		Accuracy neutral: 81%
		Accuracy negative: 75%
	DS: 50 (50% agreement) - Length 4846
		Accuracy positive: 85%
		Accuracy neutral: 78%
		Accuracy negative: 75%

Parser module:
	- parses given text and outputs a list of tokens (leading, positive, lagging:up, etc) along with list of words that represent those tokens
	  for evaluation purposes
	- it splits the text into words (using nltk module) and searches in loaded dictionaries proposed indicators
	- it also groups performance indicators together with directionality words (ex: leading:down)

Trainer Module:
	- train method in Trainer class trains the model on a given dataset of labeled sentences, it outputs a dictionary simmilar with the one described above which is used as a model
	- evaluate method evaluates the model on a dataset similar with one used for training, it computes the accuracy (correctly guessed / total sentences)

Api Module:
	- exposes a function to be used on any text, the module can be executed on a text file and will output a percentage of sentiment for the text inside the file

Config module:
	- used to set paths


Improvements made:

	In order to improve and boost the performance of the model lagging-rev was introduced. It splits lagging words from those that would give another polarity if combined with same directionality word. For example: "costs increase" (lagging:up) is actually mapped to negative unlike "earnings increase" (lagging:up) which is clerly mapped positive

	Also dictionaries were slightly modified:
		Following words were added:
			- negative: struggles scamming scam scammer struggling struggle
			- directionality: boosted awarded violate upgraded raise quadruple increased narrow saved liquidate more dropped terminate surged downgraded 
					decreased multiplied losing gained hiked recruited falling recommend reduced climbed recommended outperformed signed save lowest warnings
					declined struggled speed swinged shutted violates double triple surpassed burden improved struggles plunge expanded slipped
			- lagging-rev: expenses loss cost operating cost net loss operating expense operating loss costs tax expense taxes
		
		Following words were removed:
			- negative: restructuring closed bridge disclose force diverted closing disclosed concern
			- positive: enables effective invention inventors
			- lagging: expenses loss cost operating cost net loss operating expense operating loss costs tax expense taxes 

Future work:
	Introduction of numbers comparison:
		Ex: The diluted loss per share narrowed to EUR 0.27 from EUR 0.86
			Return on investment was 16.6 % compared to 15.8 % in 2004
			Net profit was 35.5 mln compared with 29.8 mln

	Introducing phrasal-verbs dictionary:
		Ex: Small investors have voiced fears that the shares will end up with risk investors
			("up" is marked as directionality word where in fact it's part of "end up")