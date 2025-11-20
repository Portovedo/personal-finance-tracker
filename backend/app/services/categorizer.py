import logging
import pickle
import os
from typing import List, Optional
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.category import Category

logger = logging.getLogger(__name__)

# Path relative to where the app runs (dist folder in production)
MODEL_PATH = "app/ml_models/categorizer_model.pkl"

class MLCategorizer:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info("ML Model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load ML model: {e}")
                self.model = None
        else:
            logger.info("No existing ML model found. Starting fresh.")

    def train(self, db: Session):
        transactions = db.query(Transaction).filter(Transaction.category_id.isnot(None)).all()
        
        if len(transactions) < 10:
            logger.warning("Not enough data to train ML model.")
            return

        data = []
        labels = []
        for t in transactions:
            if t.description and t.category:
                data.append(t.description)
                labels.append(t.category.name)

        if not data:
            return

        pipeline = Pipeline([
            ('vect', CountVectorizer(stop_words='english')),
            ('clf', MultinomialNB()),
        ])

        try:
            pipeline.fit(data, labels)
            self.model = pipeline
            
            os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
            with open(MODEL_PATH, 'wb') as f:
                pickle.dump(self.model, f)
            
            logger.info(f"Model trained on {len(data)} transactions.")
        except Exception as e:
            logger.error(f"Training failed: {e}")

    def predict(self, description: str) -> Optional[str]:
        if not self.model:
            return None
        try:
            prediction = self.model.predict([description])[0]
            return prediction
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return None

    def categorize(self, transaction_description: str, db: Session) -> Optional[int]:
        category_name = self.predict(transaction_description)
        if category_name:
            category = db.query(Category).filter(Category.name == category_name).first()
            if category:
                return category.id
        return None