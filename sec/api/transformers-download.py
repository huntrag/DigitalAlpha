from transformers import BertTokenizer, BertForSequenceClassification
finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
finbert.save_pretrained("C:\\Users\\Kaushik Dey\\Documents\\DigitalAlpha\\sec\\finbert-tone")
tokenizer.save_pretrained("C:\\Users\\Kaushik Dey\\Documents\\DigitalAlpha\\sec\\finbert-tone")

