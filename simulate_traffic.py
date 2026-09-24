import asyncio
import httpx
import random

OFFERS = [
    {"offer_id": "crypto_scam_01", "title": "Elon Musk's Quantum AI Trading App", "description": "Guaranteed 500% returns in 3 days. Deposit  now and become a millionaire. Open to EU and AU residents."},
    {"offer_id": "nutra_magic_01", "title": "Keto Burn Xtreme: Lose 20kg in 1 week without diet!", "description": "Miracle pill used by celebrities. 100% natural, FDA approved (fake claim). Buy 1 get 2 free!"},
    {"offer_id": "ecom_nike_sale", "title": "Nike Air Max Spring Clearance", "description": "Official partner. 30% off all Air Max shoes. Target: US, UK, DE. Payout: 15% revshare."},
    {"offer_id": "igaming_casino_01", "title": "SpinWin Casino: 200 Free Spins + 100% Deposit Match", "description": "New licensed casino in Brazil. Target audience: Men 21+. CPA:  per first time deposit."},
    {"offer_id": "dating_mainstream", "title": "Tinder Gold Subscription - Free Trial", "description": "Promote our special 1-week free trial for Tinder Gold. Target: WW (Worldwide)."},
    {"offer_id": "crypto_scam_02", "title": "Secret Bitcoin Loophole - Banks Hate This", "description": "This newly discovered loophole makes  a day automatically. Just send your initial investment to our broker."},
    {"offer_id": "nutra_joint_cream", "title": "Flekosteel Joint and Muscle Balm", "description": "High converting offer in LATAM. Helps with muscle tension and joint discomfort. COD (Cash on Delivery) model."},
    {"offer_id": "finance_cc", "title": "Chase Sapphire Preferred Credit Card", "description": "Earn 60,000 bonus points after you spend ,000 on purchases in the first 3 months. US ONLY."},
    {"offer_id": "sweepstakes_iphone", "title": "Win a Free iPhone 16 Pro Max!", "description": "Enter your email and credit card details for a chance to win. High risk rebill offer."},
    {"offer_id": "igaming_betting", "title": "Bet365 Sportsbook: Bet  Get ", "description": "Promote legal sports betting in US states (NJ, PA, OH, VA). Strict compliance required."},
]

async def send_offer(client, offer):
    url = "http://127.0.0.1:8000/api/v1/offers/process"
    try:
        response = await client.post(url, json=offer)
        print(f"Sent {offer['offer_id']}: {response.status_code}")
    except Exception as e:
        print(f"Error sending {offer['offer_id']}: {e}")

async def main():
    print("Starting traffic simulation...")
    async with httpx.AsyncClient() as client:
        tasks = [send_offer(client, offer) for offer in OFFERS]
        await asyncio.gather(*tasks)
    print("Simulation complete! Check Celery logs to see the AI evaluating them in parallel.")

if __name__ == '__main__':
    asyncio.run(main())
