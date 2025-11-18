from semantic_router import Route
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.routers import SemanticRouter  # <-- use this instead of RouteLayer

encoder = HuggingFaceEncoder(name="sentence-transformers/all-MiniLM-L6-v2")

faq = Route(
    name='faq',
    utterances=[
        # Return policy
        "What is the return policy?",
        "Can I return my order?",
        "How many days do I have to return?",
        "What's your return window?",

        # Discounts
        "Do I get any discount with my card?",
        "Are there discounts for HDFC customers?",
        "What credit card offers do you have?",
        "Any bank offers available?",

        # Order tracking
        "How can I track my order?",
        "Where is my package?",
        "How do I check order status?",
        "Track my delivery",

        # Payment methods
        "What payment options do you accept?",
        "Can I pay with UPI?",
        "Do you accept cash on delivery?",
        "Which payment methods are available?",

        # Refunds
        "How long does refund take?",
        "When will I get my money back?",
        "Refund processing time?",
        "How soon is the refund?",

        # Sales and promotions
        "Are there any sales going on?",
        "Do you have any offers?",
        "What promotions are available?",
        "Any discounts right now?",

        # Order modification
        "Can I cancel my order?",
        "How do I modify my order?",
        "Can I change my order after placing?",
        "Cancel order",

        # Shipping
        "Do you ship internationally?",
        "Can you deliver to other countries?",
        "International shipping available?",
        "Do you ship outside India?",

        # Damaged products
        "I received a damaged product",
        "My order arrived broken",
        "What if the product is defective?",
        "Damaged item received",

        # Promo codes
        "How do I apply promo code?",
        "Where do I enter coupon code?",
        "How to use discount code?",
        "Apply promo code at checkout"
    ]
)

sql = Route(
    name="sql",
    utterances=[
        # ORIGINALS (improved slightly for clarity)
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",

        # PRICE FILTERS
        "Show me shoes cheaper than 2000.",
        "What are the best shoes under 1500?",
        "List products below 1000.",
        "Any premium shoes above 5000?",
        "Find me shoes priced between 2000 and 4000.",

        # BRAND FILTERS
        "Show all Adidas shoes.",
        "Do you have Reebok running shoes?",
        "Find me Woodland boots.",
        "Show Puma products rated above 4 stars.",

        # DISCOUNT FILTERS
        "Show me items with more than 40% discount.",
        "Give me products that are on sale.",
        "Any high-discount shoes right now?",
        "List all shoes with at least 20% off.",

        # RATINGS
        "Show me top rated shoes.",
        "Give me shoes with rating more than 4.0.",
        "Any 5 star sneakers?",

        # SORTING REQUESTS
        "Give me 3 shoes in descending order of price.",
        "Show products sorted by highest discount.",
        "List items ordered by rating from high to low.",
        "Sort Adidas shoes by price ascending.",
        "Sort all footwear by newest first.",
        "Show cheapest shoes first.",
        "Show most expensive shoes first.",

        # LIMIT / TOP-N
        "Give me top 5 Puma shoes.",
        "Show 10 cheapest sneakers.",
        "I want the 3 best rated running shoes.",
        "Give me top 2 discounted products.",

        # CATEGORY FILTERS
        "Show me running shoes.",
        "Do you have loafers?",
        "Find high ankle boots.",
        "Show formal shoes for men.",

        # SIZE FILTERS
        "Give me size 8 shoes.",
        "Do you have sneakers in size 10?",
        "List size 7 footwear.",

        # COMBINATIONS
        "Show me Nike shoes under 3000 sorted by rating.",
        "Give me Adidas running shoes with discount above 20%.",
        "Show 5 Puma shoes below 2000.",
        "Find Nike sneakers above 4.2 rating with at least 10% discount.",
        "Give me formal shoes size 9 under 2500.",

        # AVAILABILITY
        "Show items in stock.",
        "Which shoes are available?",
        "List products currently available.",

        # GENERAL
        "Find me some affordable shoes.",
        "I want good running shoes.",
        "Show me the newest items.",
        "Give me products I might like.",
    ]
)

small_talk = Route(
    name="small_talk",
    utterances=[
        # Basic greetings
        "Hi",
        "Hello",
        "Hey",
        "Hey there",
        "Hi bro",

        # How-are-you variations
        "How are you?",
        "How you doing?",
        "You good?",
        "How’s it going?",

        # Identity questions
        "What is your name?",
        "Who are you?",
        "Are you a robot?",
        "Are you human?",
        "What are you?",

        # Purpose questions
        "What do you do?",
        "What is your job?",
        "Why are you here?",
        "What can you do?",

        # Random small talk
        "Tell me something about yourself",
        "Can we talk?",
        "I want to chat",
        "Are you alive?",
        "Do you understand me?",

        "Hi", "Hello", "Hey", "Hey there", "Hi there", "Good morning", "Good evening", "Howdy",

        # asking about well-being
        "How are you?", "How are you doing?", "How are you feeling?", "How's it going?", "How are you today?", "You feeling good?",

        # asking about identity
        "What is your name?", "Who are you?", "What are you?", "Are you a robot?", "Are you human?",

        # asking about purpose
        "What do you do?", "What can you do?", "Can you help me?", "Tell me about yourself",

        # casual chatter
        "What's up?", "What's new?", "How's everything?", "How's your day?", "How's life?", "Sup?"

    ]
)


router = SemanticRouter(encoder=encoder, routes=[faq, sql, small_talk], auto_sync="local")

if __name__ == "__main__":
    print(router("What is your policy on defective product?").name)
    print(router("Pink Puma shoes in price range 5000 to 1000").name)
