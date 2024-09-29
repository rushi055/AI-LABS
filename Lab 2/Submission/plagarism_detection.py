import heapq

# Step 1: Text Preprocessing without using re
def preprocess_text(text):
    # Tokenize by splitting on periods (naive approach for sentence splitting)
    sentences = text.split('.')

    # Remove any trailing spaces or empty sentences and normalize to lowercase
    sentences = [sentence.strip().lower() for sentence in sentences if sentence.strip()]

    # Further remove punctuation using string methods
    normalized_sentences = []
    for sentence in sentences:
        # Remove punctuation characters manually
        sentence = ''.join([char for char in sentence if char.isalnum() or char.isspace()])
        normalized_sentences.append(sentence)

    return normalized_sentences

# Step 2: Edit Distance (Levenshtein Distance)
def edit_distance(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Initialize dp table
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    # Fill dp table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[n][m]

# Step 3: A* Search Algorithm for Sentence Alignment
def a_star_alignment(doc1, doc2, skip_penalty=5):
    n, m = len(doc1), len(doc2)
    
    # Priority queue (min-heap) for A* search
    heap = []
    # State: (total_cost, g(n) - cost so far, i, j, alignment path)
    heapq.heappush(heap, (0, 0, 0, 0, []))  # Initial state
    
    # Visited set to track explored states
    visited = set()
    
    # Heuristic function: optimistic estimate of remaining alignment cost
    def heuristic(i, j):
        # Minimum possible edit distance between remaining sentences
        remaining_doc1 = doc1[i:]
        remaining_doc2 = doc2[j:]
        h = 0
        min_len = min(len(remaining_doc1), len(remaining_doc2))
        for k in range(min_len):
            h += edit_distance(remaining_doc1[k], remaining_doc2[k])
        return h
    
    # A* Search loop
    while heap:
        total_cost, g_cost, i, j, path = heapq.heappop(heap)
        
        # Goal state reached (aligned all sentences)
        if i == n and j == m:
            return total_cost, path
        
        # Avoid revisiting the same state
        if (i, j) in visited:
            continue
        visited.add((i, j))
        
        # Transitions (Align current sentences, skip in one or both documents)
        if i < n and j < m:
            # Align current sentence i in doc1 with sentence j in doc2
            align_cost = edit_distance(doc1[i], doc2[j])
            heapq.heappush(heap, (
                g_cost + align_cost + heuristic(i + 1, j + 1), 
                g_cost + align_cost, 
                i + 1, j + 1, 
                path + [(i, j)]
            ))
        
        if i < n:
            # Skip current sentence in doc1
            heapq.heappush(heap, (
                g_cost + skip_penalty + heuristic(i + 1, j), 
                g_cost + skip_penalty, 
                i + 1, j, 
                path + [(i, None)]
            ))
        
        if j < m:
            # Skip current sentence in doc2
            heapq.heappush(heap, (
                g_cost + skip_penalty + heuristic(i, j + 1), 
                g_cost + skip_penalty, 
                i, j + 1, 
                path + [(None, j)]
            ))
        
        if i < n and j < m:
            # Skip current sentences in both documents
            heapq.heappush(heap, (
                g_cost + skip_penalty + heuristic(i + 1, j + 1), 
                g_cost + skip_penalty, 
                i + 1, j + 1, 
                path + [(None, None)]
            ))

    # Return failure if no alignment found
    return float('inf'), []

# Step 4: Detect Plagiarism
def detect_plagiarism(alignment, doc1, doc2, threshold=10):
    plagiarized_pairs = []
    
    for i, j in alignment:
        if i is not None and j is not None:
            cost = edit_distance(doc1[i], doc2[j])
            if cost <= threshold:  # Low edit distance implies potential plagiarism
                plagiarized_pairs.append((i, j, cost))
    
    return plagiarized_pairs

# Step 5: Final Plagiarism Classification
def classify_plagiarism(plagiarized_pairs, total_sentences, threshold=0.5):
    plagiarized_count = len(plagiarized_pairs)
    
    if plagiarized_count / total_sentences > threshold:
        return "Plagiarism"
    elif plagiarized_count > 0:
        return "Partial Plagiarism"
    else:
        return "No Plagiarism"

# Step 6: Evaluation (Test Cases)
def evaluate_system(doc1, doc2, threshold=10, skip_penalty=5):
    # Preprocess the documents
    processed_doc1 = preprocess_text(doc1)
    processed_doc2 = preprocess_text(doc2)

    # Perform A* search for alignment
    cost, alignment = a_star_alignment(processed_doc1, processed_doc2, skip_penalty)
    
    # Detect plagiarism based on alignment
    plagiarized_pairs = detect_plagiarism(alignment, processed_doc1, processed_doc2, threshold)
    
    # Classification of plagiarism level
    total_sentences = max(len(processed_doc1), len(processed_doc2))
    plagiarism_classification = classify_plagiarism(plagiarized_pairs, total_sentences)
    
    # Output results
    print(f"Total alignment cost: {cost}")
    print("Plagiarized Sentence Pairs:")
    for i, j, cost in plagiarized_pairs:
        print(f"Doc1 (Sentence {i+1}): {processed_doc1[i]} | Doc2 (Sentence {j+1}): {processed_doc2[j]} (Edit Distance: {cost})")
    
    # Final Classification
    print(f"Plagiarism Classification: {plagiarism_classification}")

# Example Test Case
doc1 = """
This is the first sentence. This is the second sentence. Another sentence is here.
"""
doc2 = """
This is the first sentence. A different second sentence appears here. Another sentence here.
"""

# Step 7: Run evaluation with the example documents
evaluate_system(doc1, doc2, threshold=10, skip_penalty=5)
