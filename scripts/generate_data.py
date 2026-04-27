from faker import Faker
import random
import json

fake_en = Faker()
fake_ar = Faker("ar_EG")

PRODUCTS = [
    "Baby Stroller",
    "Feeding Bottle",
    "Diapers",
    "Baby Monitor",
    "Car Seat"
]

PROS = [
    "easy to use", "good quality", "durable", "comfortable", "value for money"
]

CONS = [
    "too expensive", "poor quality", "broke quickly", "not comfortable", "bad packaging"
]

AR_PROS = [
    "جودة عالية", "سهل الاستخدام", "مريح", "ممتاز", "قيمة جيدة"
]

AR_CONS = [
    "غالي جدا", "جودة سيئة", "انكسر بسرعة", "غير مريح", "تغليف سيء"
]


def generate_review():
    is_arabic = random.choice([True, False])

    sentiment = random.choice(["positive", "negative", "neutral"])

    if is_arabic:
        text = fake_ar.sentence()
        if sentiment == "positive":
            text += " " + random.choice(AR_PROS)
        elif sentiment == "negative":
            text += " " + random.choice(AR_CONS)
    else:
        text = fake_en.sentence()
        if sentiment == "positive":
            text += " " + random.choice(PROS)
        elif sentiment == "negative":
            text += " " + random.choice(CONS)

    # Add noise
    if random.random() < 0.2:
        text += " 😡"
    if random.random() < 0.2:
        text = text.lower()

    return {
        "review_id": fake_en.uuid4(),
        "product": random.choice(PRODUCTS),
        "rating": random.randint(1, 5),
        "text": text,
        "language": "ar" if is_arabic else "en"
    }


def generate_dataset(n=200):
    return [generate_review() for _ in range(n)]


if __name__ == "__main__":
    data = generate_dataset(200)

    with open("../data/raw_reviews.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Dataset generated successfully!")