import random
import time


def generate_story(name, city, state, gender, niche):
    """
    Generate a personalized bio/story for a content creator in the 'fashion' or 'beauty' niche.
    """

    # Introduction Variations
    introductions = [
        f"Hey there! I’m {name}, a passionate content creator from {city}, {state}.",
        f"Hello! My name is {name}, and I bring creative energy straight from {city}, {state}.",
        f"Hi, I’m {name}, your go-to {niche} expert from {city}, {state}!",
        f"Welcome to my world! I’m {name}, a creator deeply inspired by {niche}.",
        f"Hi, I’m {name} from {city}, and I’m here to make {niche} fun and exciting!",
        f"Hey, I’m {name} from {city}! Creating {niche} content is my absolute passion.",
        f"Hi, I’m {name}, and I turn everyday moments into inspiring {niche} stories!",
        f"Welcome! I’m {name} from {city}, {state}, ready to take you on a {niche} journey!",
        f"Hello! I’m {name}, and I believe {niche} is all about creativity and confidence.",
        f"Hey everyone! {name} here, bringing fresh and exciting {niche} ideas your way!",
        f"Hi there! I’m {name} from {city}, and I’m obsessed with all things {niche}!",
        f"Hey, I’m {name}—just a {niche} lover from {city}, making content with passion.",
        f"Hi, I’m {name}! From {city}, I create fun and inspiring {niche} content every day.",
        f"Hello, my name is {name}! Let’s explore the world of {niche} together!",
        f"Hey, I’m {name}, your friendly {niche} enthusiast from {city}, {state}!",
        f"Hi, I’m {name}! {niche} is my creative outlet, and I’m here to share it with you!",
        f"Hey there! I’m {name}, a {niche} content creator, turning ideas into inspiration!",
        f"Welcome! I’m {name} from {city}, and I love making {niche} more exciting for you.",
        f"Hi, I’m {name}! Join me on a creative journey through the world of {niche}!",
        f"Hey, I’m {name}—sharing my passion for {niche} straight from {city}, {state}!",
        f"Hello, I’m {name}, and I believe {niche} is the perfect way to express yourself!",
        f"Hey! I’m {name}, your {niche} guide from {city}, and I love sharing my best finds!",
        f"Hi, I’m {name}, a storyteller at heart, bringing the magic of {niche} to life!",
        f"Hey, I’m {name}! Let’s dive into the world of {niche} and create something amazing.",
        f"Hi there! I’m {name}, and my goal is to make {niche} content both fun and useful!"
    ]



    # Middle Section Variations (Based on Niche)
    middle_section = {
        "fashion": [
            f"Where I fell in love with styling and fashion trends. 💃",
            f"My journey started in {city}, experimenting with bold outfits and trendy styles. 👗",
            f"I discovered the magic of mixing and matching unique fashion pieces! 🎽",
            f"I believe fashion is more than clothes—it’s self-expression! That’s what I share. 🕶️",
            f"From thrift finds to high-end couture, I love exploring every style possible!",
            f"Fashion isn’t just my passion—it’s my way of helping others express confidence. 💫",
            f"Whether it’s street style or luxury fashion, I love bringing creative looks to life! 👜",
            f"My biggest joy is inspiring confidence through effortless yet stylish outfits! ✨",
            f"Fashion allows me to tell stories through clothing, and I’m excited to share them with you!",
            f"Styling is like an art form, and I can’t wait to help you unlock your unique fashion sense!",
            f"I’m always on the lookout for fresh trends and timeless pieces to create the perfect look! 🔥",
            f"Every outfit has a story, and I love curating looks that inspire confidence and creativity! 🥻",
            f"Fashion is about being bold, expressive, and unapologetically yourself—I love sharing that! 🎨",
            f"My style philosophy? Comfort meets chic, with a touch of personality in every look. 🌟",
            f"I love exploring different cultures through fashion—each style tells a unique story. 🌍",
            f"Mixing patterns, colors, and textures is my fashion playground, and I love experimenting! 🎭",
            f"From runway trends to everyday essentials, I break down the best in fashion for you! 🏆",
            f"Fashion is ever-changing, and I’m here to guide you through every exciting trend! 🔄",
            f"My goal is to help you embrace your own fashion journey with confidence and style! 💃",
            f"Finding your personal style should be fun and expressive, and I’m here to make it easier! 💡"
        ],
        "beauty": [
            f"From my early days , I explored the world of skincare and makeup. 💄",
            f"I’ve always loved experimenting with beauty products, and now I share my best tips!",
            f"My journey into beauty started in {city}, where I learned the art of self-care. ✨",
            f"Healthy skin and stunning makeup looks are my obsession—I love sharing them! 💕",
            f"Beauty is about feeling good in your own skin, and I’m here to make it easier for you!",
            f"From natural skincare to bold glam looks, I’m here to help you glow inside and out! 🌟",
            f"I love breaking down beauty trends and making them easy for everyone to try. 💋",
            f"My passion is to help you discover the best beauty routines that truly work for you!",
            f"Beauty isn’t just about products—it’s about confidence, self-love, and self-care!",
            f"I explore everything from timeless beauty secrets to the latest trends—let’s glow together!",
            f"Perfecting my skincare routine in {city} led me to discover my love for beauty! 🌿",
            f"Whether it’s a subtle no-makeup look or full-glam, I love creating beauty magic! ✨",
            f"I’m always testing the best beauty products so you don’t have to—only the best for you! 🏆",
            f"From drugstore gems to luxury must-haves, I love sharing what really works in beauty! 💎",
            f"Beauty is a journey, and I’m here to guide you to your best, most confident self! 🚀",
            f"Exploring beauty trends in {city} opened my eyes to the power of self-expression. 💖",
            f"Makeup isn’t just about looking good—it’s about having fun and feeling amazing! 🎨",
            f"Your beauty routine should be effortless and fun, and I’m here to help with that! 🌟",
            f"Let’s break down beauty myths, find holy-grail products, and glow together! 💫",
            f"I love helping people find beauty routines that fit their lifestyle—simple, yet stunning! 🌸"
        ]
    }

    conclusions = [
        "Join me as I share my experiences, tips, and secrets to help you shine! ✨",
        "Follow along for amazing insights and inspiration in the world of {niche}.",
        "Let's explore the best of {niche} together—one step at a time! 🚀",
        "Every post is crafted with love to bring you the best of {niche}—let’s grow together! ❤️",
        "Let’s embrace creativity and confidence in {niche}! Follow me for endless inspiration.",
        "Can’t wait to take you on this exciting journey of {niche}—let’s get started! 🎉",
        "Your unique journey in {niche} starts here—let’s make it a memorable one!",
        "There’s so much to discover in {niche}—let’s make every moment count! 🌈",
        "Stay connected and inspired as we dive deeper into the world of {niche}! 💡",
        "Follow me for expert tips, personal stories, and everything you need to master {niche}.",
        "Let’s build a community where passion for {niche} brings us all together! 💬",
        "Excited to share my knowledge and learn from you too—let’s grow in {niche} together! 🌱",
        "Every journey in {niche} is unique—let’s embrace yours and make it special! ✨",
        "Here’s to new adventures, discoveries, and growth in {niche}! Let’s go! 🚀",
        "My goal is to inspire, educate, and entertain—let’s make {niche} fun and fulfilling! 🎭",
        "Let’s make every step in {niche} more exciting and rewarding—follow for more! 👏",
        "The best part of {niche}? We’re in it together! Let’s learn, create, and grow. 💡",
        "Your passion for {niche} deserves the best—let’s keep the creativity flowing! 🎨",
        "Join me on this inspiring ride through {niche}, where every moment counts! 🎢",
        "This is just the beginning—let’s explore, experiment, and thrive in {niche} together! 💪"
    ]

    # Generate a random story
    story = (
        f"{random.choice(introductions)} "
        f"{random.choice(middle_section.get(niche, middle_section['fashion']))} "
        f"{random.choice(conclusions).format(niche=niche)}"
    )

    return story



def call():
    # Example Usage:
    name = "Sophia"
    city = "New York"
    address1 = "Brooklyn Heights"
    state = "NY"
    gender = "Female"
    nicheValue = "fashion"

    story = generate_story(name, city, state, gender, nicheValue)
    time.sleep(2)  # Simulating delay
    print(story)


# for i in range (10):
#     call()
#     print("\n")


