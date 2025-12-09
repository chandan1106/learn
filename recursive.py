import sys
from functools import lru_cache

# We must increase recursion limit for deep trees
sys.setrecursionlimit(2000)

# --- THE DATA ---
# Token costs (Weights)
doc_tokens = [10, 20, 30, 40, 50, 10, 20, 15, 5, 5]
# Relevance Scores (Values)
doc_scores = [60, 100, 120, 150, 200, 50, 80, 90, 30, 20]
# Max Context Window (Capacity)
MAX_TOKENS = 50

# --- THE ENGINE ---
# We wrap the function in a class or closure to hold data, 
# or pass data as tuples to make them hashable for cache.
# Here, we keep it simple with global scope for demo.

@lru_cache(maxsize=None)
def knapsack_memo(n, capacity):
    # Base Case
    if n == 0 or capacity == 0:
        return 0
    
    current_weight = doc_tokens[n-1]
    current_val = doc_scores[n-1]
    
    # If too heavy, skip
    if current_weight > capacity:
        return knapsack_memo(n-1, capacity)
    
    # Max(Skip, Take)
    else:
        # Skip
        val_skip = knapsack_memo(n-1, capacity)
        # Take
        val_take = current_val + knapsack_memo(n-1, capacity - current_weight)
        
        return max(val_skip, val_take)

# --- EXECUTION ---
print("--- STARTING CONTEXT OPTIMIZATION ---")
print(f"Documents Available: {len(doc_tokens)}")
print(f"Max Context Window: {MAX_TOKENS} tokens")

n_items = len(doc_tokens)
max_relevance = knapsack_memo(n_items, MAX_TOKENS)

print(f"\n MAXIMUM RELEVANCE SCORE POSSIBLE: {max_relevance}")

# For verification:
# One optimal combo for 50 capacity:
# 20 tokens (100 score) + 10 tokens (60 score) + 15 tokens (90 score) + 5 tokens (30 score)
# Total Tokens: 50 | Total Score: 280
# (The algo might find an even better one, let's see)