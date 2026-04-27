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

EN_TEMPLATES = [
    "This {product} is very {quality}",
    "I bought this {product} and it is {quality}",
    "For my baby, this {product} is {quality}",
]

AR_TEMPLATES = [
    "هذا {product} {quality}",
    "اشتريت هذا {product} وهو {quality}",
    "هذا {product} لطفلي و {quality}",
]


def generate_review():
    product = random.choice(PRODUCTS)
    is_arabic = random.choice([True, False])
    sentiment = random.choice(["positive", "negative", "neutral"])

    # Choose quality word
    if sentiment == "positive":
        quality_en = random.choice(PROS)
        quality_ar = random.choice(AR_PROS)
    elif sentiment == "negative":
        quality_en = random.choice(CONS)
        quality_ar = random.choice(AR_CONS)
    else:
        quality_en = "okay"
        quality_ar = "عادي"

    # Generate base text
    if is_arabic:
        text = random.choice(AR_TEMPLATES).format(
            product=product,
            quality=quality_ar
        )
    else:
        text = random.choice(EN_TEMPLATES).format(
            product=product,
            quality=quality_en
        )

    # Add realistic noise
    if random.random() < 0.2:
        text += " " + fake_en.word()  # random word noise

    if random.random() < 0.15:
        text += " 😡"

    if random.random() < 0.15:
        text = text.lower()

    # Add contradictory signals (important for eval)
    if random.random() < 0.1:
        text += " but also not comfortable"

    # Add mixed language (very important)
    if random.random() < 0.1:
        text += " good quality"

    return {
        "review_id": fake_en.uuid4(),
        "product": product,
        "rating": random.randint(1, 5),
        "text": text,
        "language": "ar" if is_arabic else "en"
    }


def generate_dataset(n=200):
    data = [generate_review() for _ in range(n)]

    # Add duplicates (real-world scenario)
    data.extend(random.sample(data, k=int(0.1 * n)))

    # Add garbage inputs (for robustness testing)
    data.append({
        "review_id": fake_en.uuid4(),
        "product": "Baby Stroller",
        "rating": 3,
        "text": "",
        "language": "en"
    })

    data.append({
        "review_id": fake_en.uuid4(),
        "product": "Baby Stroller",
        "rating": 1,
        "text": "????",
        "language": "en"
    })

    return data


if __name__ == "__main__":
    data = generate_dataset(200)

    with open("../data/raw_reviews.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Dataset generated successfully! Total reviews: {len(data)}")