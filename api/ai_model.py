# # import torch
# # from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
# # import pandas as pd
# # import random

# # class DreamGenerator:
# #     def __init__(self, model_path, dataset_path):
# #         # Load trained model and tokenizer
# #         self.tokenizer = DistilBertTokenizer.from_pretrained(model_path)
# #         self.model = DistilBertForSequenceClassification.from_pretrained(model_path)
# #         self.model.eval()
# #         # Load dataset
# #         self.df = pd.read_csv(dataset_path)
# #         self.emotion_map = {"Positive": 0, "Negative": 1, "Neutral": 2, "Bittersweet": 3}

# #     def classify_emotion(self, prompt):
# #         # Tokenize and predict emotion
# #         inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, padding=True, max_length=128)
# #         with torch.no_grad():
# #             outputs = self.model(**inputs)
# #             logits = outputs.logits
# #             predicted_class = torch.argmax(logits, dim=1).item()
# #         # Reverse map to emotion label
# #         for emotion, idx in self.emotion_map.items():
# #             if idx == predicted_class:
# #                 return emotion
# #         return "Neutral"  # Default fallback

# #     def generate_dream(self, prompt):
# #         # Step 1: Classify emotion
# #         emotion = self.classify_emotion(prompt)
        
# #         # Step 2: Filter dataset by emotion
# #         emotion_df = self.df[self.df["Emotion"] == emotion]
# #         if emotion_df.empty:
# #             return f"A dream inspired by '{prompt}': A vague, shifting scene unfolds..."

# #         # Step 3: Randomly select a row and adapt its Prompt column
# #         row = emotion_df.sample(n=1).iloc[0]
# #         base_dream = row["Prompt"]
        
# #         # Step 4: Incorporate user prompt into the dream (simple concatenation for now)
# #         dream_output = f"{base_dream}, woven with echoes of '{prompt}'."
# #         return dream_output

# # # Initialize model (load once at server start)
# # dream_generator = DreamGenerator(
# #     model_path="./dreamcrafter_model",
# #     dataset_path="./api/dreamcrafter_dataset.csv"
# # )


# # api/ai_model.py
# import torch
# from transformers import GPT2LMHeadModel, GPT2Tokenizer, DistilBertTokenizer, DistilBertForSequenceClassification

# class DreamGenerator:
#     def __init__(self, bert_model_path, gpt2_model_path):
#         # Load DistilBERT for emotion classification
#         self.bert_tokenizer = DistilBertTokenizer.from_pretrained(bert_model_path)
#         self.bert_model = DistilBertForSequenceClassification.from_pretrained(bert_model_path)
#         self.bert_model.eval()
#         self.emotion_map = {"Positive": 0, "Negative": 1, "Neutral": 2, "Bittersweet": 3}

#         # Load GPT-2 for dream generation
#         self.gpt2_tokenizer = GPT2Tokenizer.from_pretrained(gpt2_model_path)
#         self.gpt2_model = GPT2LMHeadModel.from_pretrained(gpt2_model_path)
#         self.gpt2_model.eval()

#     def classify_emotion(self, prompt):
#         inputs = self.bert_tokenizer(prompt, return_tensors="pt", truncation=True, padding=True, max_length=128)
#         with torch.no_grad():
#             outputs = self.bert_model(**inputs)
#             predicted_class = torch.argmax(outputs.logits, dim=1).item()
#         return next((emo for emo, idx in self.emotion_map.items() if idx == predicted_class), "Neutral")

#     def generate_dream(self, prompt):
#         emotion = self.classify_emotion(prompt)
#         input_text = f"{emotion} dream: {prompt}"
#         inputs = self.gpt2_tokenizer.encode(input_text, return_tensors="pt")
#         with torch.no_grad():
#             outputs = self.gpt2_model.generate(
#                 inputs,
#                 max_length=100,
#                 num_return_sequences=1,
#                 do_sample=True,
#                 top_k=50,
#                 top_p=0.95,
#                 temperature=0.7,
#             )
#         dream = self.gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
#         return dream

# # Initialize
# dream_generator = DreamGenerator(
#     bert_model_path="./dreamcrafter_model",
#     gpt2_model_path="./gpt2_dreamcrafter"
# )



import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, DistilBertTokenizer, DistilBertForSequenceClassification

class DreamGenerator:
    def __init__(self, bert_model_path, gpt2_model_path):
        self.bert_tokenizer = DistilBertTokenizer.from_pretrained(bert_model_path)
        self.bert_model = DistilBertForSequenceClassification.from_pretrained(bert_model_path)
        self.bert_model.eval()
        self.emotion_map = {"Positive": 0, "Negative": 1, "Neutral": 2, "Bittersweet": 3}
        self.gpt2_tokenizer = GPT2Tokenizer.from_pretrained(gpt2_model_path)
        self.gpt2_model = GPT2LMHeadModel.from_pretrained(gpt2_model_path)
        self.gpt2_model.eval()

    def classify_emotion(self, prompt):
        inputs = self.bert_tokenizer(prompt, return_tensors="pt", truncation=True, padding=True, max_length=128)
        with torch.no_grad():
            outputs = self.bert_model(**inputs)
            predicted_class = torch.argmax(outputs.logits, dim=1).item()
        return next((emo for emo, idx in self.emotion_map.items() if idx == predicted_class), "Neutral")

    def generate_dream(self, prompt, style="default"):
        emotion = self.classify_emotion(prompt)
        style_prompts = {
            "surreal": f"{emotion} surreal dream: {prompt}",
            "calm": f"{emotion} calm dream: {prompt}",
            "default": f"{emotion} dream: {prompt}"
        }
        input_text = style_prompts.get(style, style_prompts["default"])
        inputs = self.gpt2_tokenizer.encode(input_text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.gpt2_model.generate(
                inputs,
                max_length=100,
                num_return_sequences=1,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7 if style == "calm" else 1.0  # Adjust temperature for style
            )
        dream = self.gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return dream

dream_generator = DreamGenerator(
    bert_model_path="./dreamcrafter_model",
    gpt2_model_path="./gpt2_dreamcrafter"
)