import time
import random

def add_document(self, doc_content: str) -> bool:
        """
        Returns True if added to queue, False if duplicate.
        """
        index = self._get_hash_index(doc_content)
        
        with self.lock:
            # Check 1: Is the bit already set?
            if self.bit_array[index] == 1:
                print(f"[Duplicate] Skipped: {doc_content}")
                return False  # <--- EXIT IMMEDIATELY
            
            # Action 1: Mark as seen (Set the bit)
            self.bit_array[index] = 1 # <--- CRITICAL STEP YOU MISSED
            
            # Action 2: Add to queue
            self.processing_queue.append(doc_content)
            
            print(f"[Success] Added: {doc_content}")
            return True

def retry_with_backoff(retries=3, initial_delay=1):
    """
    Decorator that retries a function with exponential backoff.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            delay = initial_delay
            
            # TODO: Write a loop that runs 'retries' times
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    
                    # TODO 2: If this was the last attempt, raise the error (Don't silence it!)
                    if attempt == retries - 1:
                        print("All retries exhausted.")
                        raise e
                    
                    # TODO 3: Sleep for 'delay' seconds
                    time.sleep(delay)
                    
                    # TODO 4: Double the delay (Exponential Backoff)
                    delay *= 2
                    
        return wrapper
    return decorator

# --- HOW WE USE IT ---
@retry_with_backoff(retries=3, initial_delay=1)
def push_to_db(doc):
    # Simulate a random crash 70% of the time
    if random.random() < 0.7:
        raise ConnectionError("DB is down!")
    print(f"Document {doc} saved to DB!")

# Test it
try:
    push_to_db("Contract_v1.pdf")
except Exception:
    print("Final failure after retries.")