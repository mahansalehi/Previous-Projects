import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)

def dot_product(vec1, vec2):
    dp = 0
    for i in vec1:
        if i in vec2:
            dp += vec1[i]*vec2[i]
    
    return dp

def cosine_similarity(vec1, vec2):
    return dot_product(vec1, vec2)/(norm(vec1)*norm(vec2))
    
def unique_words(list):
    words = []
    for i in list:
        if i not in words:
            words.append(i)
                
    return words


def build_semantic_descriptors(sentences):
    semantic_descriptors = {}
    for a in range(len(sentences)):
        q = 1
        for b in unique_words(sentences[a]):
            if b not in semantic_descriptors.keys():
                semantic_descriptors[b] ={}
             
             
            for c in unique_words(sentences[a])[q:]:
                if c not in semantic_descriptors[b].keys():
                    semantic_descriptors[b][c] = 1
                    if c not in semantic_descriptors.keys():
                        semantic_descriptors[c] = {}
                        
                    semantic_descriptors[c][b] = semantic_descriptors[b][c]
                        
                else:
                    semantic_descriptors[b][c] += 1
                    if c not in semantic_descriptors.keys():
                        semantic_descriptors[c] = {}
                            
                    semantic_descriptors[c][b] = semantic_descriptors[b][c]
                
            
            q += 1
            
        
            
    return semantic_descriptors


def build_semantic_descriptors_from_files(filenames):
    all_sentences = []
    for a in range(len(filenames)):
        f = open(filenames[a], "r", encoding="utf-8")
        text = f.read()
        text = text.lower()
        text = text.replace("!", ".")
        text = text.replace("?", ".")
        text = text.replace("-", "")
        text = text.replace("--", "")
        text = text.replace(",", "")
        text = text.replace(":", "")
        text = text.replace("'", "")
        text = text.replace(";", "")
        text = text.replace('"', '')
        sentences = text.split(".")
        for i in range(len(sentences)-1):
            sentences[i] = sentences[i].split()
                        
        all_sentences += sentences
        
        
    return build_semantic_descriptors(all_sentences)
    
def build_semantic_descriptors_from_files_percent(filenames, percent):
    all_sentences = []
    for a in range(len(filenames)):
        f = open(filenames[a], "r", encoding="utf-8")
        text = f.read()
        text = text.lower()
        text = text.replace("!", ".")
        text = text.replace("?", ".")
        text = text.replace("-", "")
        text = text.replace("--", "")
        text = text.replace(",", "")
        text = text.replace(":", "")
        text = text.replace("'", "")
        text = text.replace(";", "")
        text = text.replace('"', '')
        sentences = text.split(".")
        for i in range(len(sentences)-1):
            sentences[i] = sentences[i].split()
            
        sentences = sentences[:int(percent*(len(sentences)-1))]
                        
        all_sentences += sentences
        
        
    return build_semantic_descriptors(all_sentences)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if word not in semantic_descriptors.keys():
        return - 1
    
    else:
        vec1 = semantic_descriptors[word]
        max_similarity = None
        best_choice = None
        for i in choices:
            if i in semantic_descriptors.keys():
                vec2 = semantic_descriptors[i]
                
                if max_similarity == None:
                    max_similarity = similarity_fn(vec1, vec2)
                    best_choice = i 
                
                if similarity_fn(vec1, vec2) > max_similarity:
                    max_similarity = similarity_fn(vec1, vec2)
                    best_choice = i
                
                
                
        return best_choice
         


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    f = open(filename, encoding="utf-8")
    text = f.read()
    text = text.lower()
    sentence = text.split("\n")
    del(sentence[-1])
    for i in range(len(sentence)):
        sentence[i] = sentence[i].split() 
    
    counter = 0
    for j in sentence:
        if j[1] == most_similar_word(j[0], j[2:], semantic_descriptors, similarity_fn):
            counter += 1

            
    return (counter/len(sentence))*100
    

def test_function(percent):    
    import os 
    os.chdir("C:\\Users\\Dexter\\Desktop")
    filenames = ["Swann's_Way.txt", "War_and_Peace.txt"]
    import time 
    t1 = time.time()
    semantic_descriptors = build_semantic_descriptors_from_files_percent(filenames, percent)
    t2 = time.time()
    list = []
    '''
    for i in semantic_descriptors:
        if semantic_descriptors[i] == {}:
            list.append(i)
            
    for i in list:
        del(semantic_descriptors[i])
        '''
    print(run_similarity_test("text.txt", semantic_descriptors, cosine_similarity))
    print(t2-t1)
    return 
    
    
def euc_similarity(vec1, vec2):
    vec3 = {}
    for i in vec1:
        if i in vec2:
            vec3[i] = vec1[i] - vec2[i]
            
    return -norm(vec3)
    
def euc_norm_similarity(vec1, vec2):
    vec3 = {}
    for i in vec1:
        if i in vec2:
            vec3[i] = vec1[i]/norm(vec1) - vec2[i]/norm(vec2)
            
    return -norm(vec3)

if __name__ == '__main__':
    import os 
    os.chdir("C:\\Users\\Mahan\\Desktop")
    filenames = ["Swann's_Way.txt", "War_and_Peace.txt"]
    t1 = time.time()
    semantic_descriptors = build_semantic_descriptors_from_files(filenames)
    t2 = time.time()
    print(t2 - t1)
    print(run_similarity_test("text.txt", semantic_descriptors, cosine_similarity))
    print(run_similarity_test("text.txt", semantic_descriptors, euc_similarity))
    print(run_similarity_test("text.txt", semantic_descriptors, euc_norm_similarity))
    
    
    print(test_function(0.1))
    print(test_function(0.2))
    print(test_function(0.3))
    print(test_function(0.4))
    print(test_function(0.5))
    print(test_function(0.6))
    print(test_function(0.7))
    print(test_function(0.8))
    print(test_function(0.9))
    print(test_function(1))
    
    