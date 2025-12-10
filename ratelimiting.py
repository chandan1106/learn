import time

# --- MOCK REDIS ---
class MockRedis:
    def __init__(self):
        self.data = {}
    def get(self, key): return self.data.get(key)
    def set(self, key, value): self.data[key] = value

# --- RATE LIMITER ---
class TokenBucketLimiter:
    def __init__(self, capacity, refill_rate):
        self.redis = MockRedis()
        self.capacity = capacity
        self.rate = refill_rate

    def allow_request(self, user_id: str) -> bool:
        now = time.time()
        token_key = f"{user_id}:tokens"
        time_key = f"{user_id}:time"
        
        current_tokens = self.redis.get(token_key)
        last_refill = self.redis.get(time_key)
        
        if current_tokens is None:
            current_tokens = self.capacity
            last_refill = now
        
        delta = now - last_refill
        tokens_to_add = delta * self.rate
        new_tokens = min(self.capacity, current_tokens + tokens_to_add)
        
        if new_tokens >= 1:
            new_tokens -= 1
            self.redis.set(token_key, new_tokens)
            self.redis.set(time_key, now)
            return True
        else:
            self.redis.set(token_key, new_tokens)
            self.redis.set(time_key, now)
            return False

# --- SIMULATION ---
print("--- INITIALIZING FIREWALL ---")
# Capacity: 5 tokens max. Refill: 1 token per second.
limiter = TokenBucketLimiter(capacity=5, refill_rate=1)

user = "hacker_bot_99"

print("\n--- PHASE 1: BURST ATTACK (10 requests instantly) ---")
allowed = 0
denied = 0

for i in range(10):
    if limiter.allow_request(user):
        print(f"Request {i+1}: Allowed")
        allowed += 1
    else:
        print(f"Request {i+1}:  BLOCKED (429 Too Many Requests)")
        denied += 1

print(f"\nStats: {allowed} Allowed (Expected 5), {denied} Blocked")

print("\n--- PHASE 2: WAITING 2 SECONDS (Refill) ---")
time.sleep(2) # Should refill roughly 2 tokens

if limiter.allow_request(user):
    print("Request after wait:  Allowed (Refill worked)")
else:
    print("Request after wait:  Failed (Refill broken)")