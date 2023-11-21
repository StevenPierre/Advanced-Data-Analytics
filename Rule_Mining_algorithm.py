latin_text = """
Sed ut perspiciatis, unde omnis iste natus error sit
voluptatem accusantium doloremque laudantium, totam
rem aperiam eaque ipsa, quae ab illo inventore
veritatis et quasi architecto beatae vitae dicta
sunt, explicabo. Nemo enim ipsam voluptatem, quia
voluptas sit, aspernatur aut odit aut fugit, sed
quia consequuntur magni dolores eos, qui ratione
voluptatem sequi nesciunt, neque porro quisquam est,
qui dolorem ipsum, quia dolor sit amet consectetur
adipisci[ng] velit, sed quia non numquam [do] eius
modi tempora inci[di]dunt, ut labore et dolore
magnam aliquam quaerat voluptatem. Ut enim ad minima
veniam, quis nostrum exercitationem ullam corporis
suscipit laboriosam, nisi ut aliquid ex ea commodi
consequatur? Quis autem vel eum iure reprehenderit,
qui in ea voluptate velit esse, quam nihil molestiae
consequatur, vel illum, qui dolorem eum fugiat, quo
voluptas nulla pariatur?

At vero eos et accusamus et iusto odio dignissimos
ducimus, qui blanditiis praesentium voluptatum
deleniti atque corrupti, quos dolores et quas
molestias excepturi sint, obcaecati cupiditate non
provident, similique sunt in culpa, qui officia
deserunt mollitia animi, id est laborum et dolorum
fuga. Et harum quidem rerum facilis est et expedita
distinctio. Nam libero tempore, cum soluta nobis est
eligendi optio, cumque nihil impedit, quo minus id,
quod maxime placeat, facere possimus, omnis voluptas
assumenda est, omnis dolor repellendus. Temporibus
autem quibusdam et aut officiis debitis aut rerum
necessitatibus saepe eveniet, ut et voluptates
repudiandae sint et molestiae non recusandae. Itaque
earum rerum hic tenetur a sapiente delectus, ut aut
reiciendis voluptatibus maiores alias consequatur
aut perferendis doloribus asperiores repellat.
"""

print("First 100 characters:\n  {} ...".format(latin_text[:100]))

def normalize_string(s):
    assert type (s) is str
    ### BEGIN SOLUTION
    essential_chars = [c for c in s.lower() if c.isalpha() or c.isspace()]
    return ''.join(essential_chars)
    ### END SOLUTION
    
# Demo:
print(latin_text[:100], "...\n=>", normalize_string(latin_text[:100]), "...")

# `normalize_string_test`: Test cell
norm_latin_text = normalize_string(latin_text)

assert type(norm_latin_text) is str
assert len(norm_latin_text) == 1694
assert all([c.isalpha() or c.isspace() for c in norm_latin_text])
assert norm_latin_text == norm_latin_text.lower()

print("\n(Passed!)")

def get_normalized_words (s):
    assert type (s) is str
    ### BEGIN SOLUTION
    return normalize_string (s).split ()
    ### END SOLUTION

# Demo:
print ("First five words:\n{}".format (get_normalized_words (latin_text)[:5]))

# `get_normalized_words_test`: Test cell
norm_latin_words = get_normalized_words(norm_latin_text)

assert len(norm_latin_words) == 250
for i, w in [(20, 'illo'), (73, 'eius'), (144, 'deleniti'), (248, 'asperiores')]:
    assert norm_latin_words[i] == w

print ("\n(Passed.)")

def make_itemsets(words):
    ### BEGIN SOLUTION
    return [set(w) for w in words]
    ### END SOLUTION
# `make_itemsets_test`: Test cell
norm_latin_itemsets = make_itemsets(norm_latin_words)

# Lists should have the same size
assert len(norm_latin_itemsets) == len(norm_latin_words)

# Test a random sample
from random import sample
for i in sample(range(len(norm_latin_words)), 5):
    print('[{}]'.format(i), norm_latin_words[i], "-->", norm_latin_itemsets[i])
    assert set(norm_latin_words[i]) == norm_latin_itemsets[i]
print("\n(Passed!)")
print (int ())
from collections import defaultdict

D2 = defaultdict (int) # Empty dictionary

D2['existing-key'] = 5 # Create one key-value pair

D2['existing-key'] += 1 # Update
D2['new-key'] += 1

print (D2)

from collections import defaultdict
from itertools import combinations # Hint!

def update_pair_counts (pair_counts, itemset):
    """
    Updates a dictionary of pair counts for
    all pairs of items in a given itemset.
    """
    assert type (pair_counts) is defaultdict

    ### BEGIN SOLUTION
    for (a, b) in combinations (itemset, 2):
        pair_counts[(a, b)] += 1
        pair_counts[(b, a)] += 1
    ### END SOLUTION
# `update_pair_counts_test`: Test cell
itemset_1 = set("error")
itemset_2 = set("dolor")
pair_counts = defaultdict(int)

update_pair_counts(pair_counts, itemset_1)
assert len(pair_counts) == 6
update_pair_counts(pair_counts, itemset_2)
assert len(pair_counts) == 16

print('"{}" + "{}"\n==> {}'.format (itemset_1, itemset_2, pair_counts))
for a, b in pair_counts:
    assert (b, a) in pair_counts
    assert pair_counts[(a, b)] == pair_counts[(b, a)]
    
print ("\n(Passed!)")

def update_item_counts(item_counts, itemset):
    ### BEGIN SOLUTION
    for a in itemset:
        item_counts[a] += 1
    ### END SOLUTION
# `update_item_counts_test`: Test cell
itemset_1 = set("error")
itemset_2 = set("dolor")

item_counts = defaultdict(int)
update_item_counts(item_counts, itemset_1)
assert len(item_counts) == 3
update_item_counts(item_counts, itemset_2)
assert len(item_counts) == 5

assert item_counts['d'] == 1
assert item_counts['e'] == 1
assert item_counts['l'] == 1
assert item_counts['o'] == 2
assert item_counts['r'] == 2

print("\n(Passed!)")

def filter_rules_by_conf (pair_counts, item_counts, threshold):
    rules = {} # (item_a, item_b) -> conf (item_a => item_b)
    ### BEGIN SOLUTION
    for (a, b) in pair_counts:
        assert a in item_counts
        conf_ab = pair_counts[(a, b)] / item_counts[a]
        if conf_ab >= threshold:
            rules[(a, b)] = conf_ab
    ### END SOLUTION
    return rules
# `filter_rules_by_conf_test`: Test cell
pair_counts = {('man', 'woman'): 5,
               ('bird', 'bee'): 3,
               ('red fish', 'blue fish'): 7}
item_counts = {'man': 7,
               'bird': 9,
               'red fish': 11}
rules = filter_rules_by_conf (pair_counts, item_counts, 0.5)
print("Found these rules:", rules)
assert ('man', 'woman') in rules
assert ('bird', 'bee') not in rules
assert ('red fish', 'blue fish') in rules
print("\n(Passed!)")

def gen_rule_str(a, b, val=None, val_fmt='{:.3f}', sep=" = "):
    text = "{} => {}".format(a, b)
    if val:
        text = "conf(" + text + ")"
        text += sep + val_fmt.format(val)
    return text

def print_rules(rules):
    if type(rules) is dict or type(rules) is defaultdict:
        from operator import itemgetter
        ordered_rules = sorted(rules.items(), key=itemgetter(1), reverse=True)
    else: # Assume rules is iterable
        ordered_rules = [((a, b), None) for a, b in rules]
    for (a, b), conf_ab in ordered_rules:
        print(gen_rule_str(a, b, conf_ab))

# Demo:
print_rules(rules)

def find_assoc_rules(receipts, threshold):
    ### BEGIN SOLUTION
    pair_counts = defaultdict(int) # (item_a, item_b) -> count
    item_counts = defaultdict(int) # item -> count
    
    for itemset in receipts:
        update_pair_counts(pair_counts, itemset)
        update_item_counts(item_counts, itemset)
    rules = filter_rules_by_conf(pair_counts, item_counts, threshold)
    return rules
    ### END SOLUTION
# `find_assoc_rules_test`: Test cell
receipts = [set('abbc'), set('ac'), set('a')]
rules = find_assoc_rules(receipts, 0.6)

print("Original receipts as itemsets:", receipts)
print("Resulting rules:")
print_rules(rules)

assert ('a', 'b') not in rules
assert ('b', 'a') in rules
assert ('a', 'c') in rules
assert ('c', 'a') in rules
assert ('b', 'c') in rules
assert ('c', 'b') not in rules

print("\n(Passed!)")

# Generate `latin_rules`:
### BEGIN SOLUTION
latin_words = get_normalized_words(latin_text)
latin_itemsets = make_itemsets(latin_words)
latin_rules = find_assoc_rules(latin_itemsets, 0.75)
### END SOLUTION

# Inspect your result:
print_rules(latin_rules)

# `latin_rules_test`: Test cell
assert len(latin_rules) == 10
assert all([0.75 <= v <= 1.0 for v in latin_rules.values()])
for ab in ['xe', 'qu', 'hi', 'xi', 'vt', 're', 've', 'fi', 'gi', 'bi']:
    assert (ab[0], ab[1]) in latin_rules
print("\n(Passed!)")

english_text = """
But I must explain to you how all this mistaken idea
of denouncing of a pleasure and praising pain was
born and I will give you a complete account of the
system, and expound the actual teachings of the great
explorer of the truth, the master-builder of human
happiness. No one rejects, dislikes, or avoids
pleasure itself, because it is pleasure, but because
those who do not know how to pursue pleasure
rationally encounter consequences that are extremely
painful. Nor again is there anyone who loves or
pursues or desires to obtain pain of itself, because
it is pain, but occasionally circumstances occur in
which toil and pain can procure him some great
pleasure. To take a trivial example, which of us
ever undertakes laborious physical exercise, except
to obtain some advantage from it? But who has any
right to find fault with a man who chooses to enjoy
a pleasure that has no annoying consequences, or
one who avoids a pain that produces no resultant
pleasure?

On the other hand, we denounce with righteous
indignation and dislike men who are so beguiled and
demoralized by the charms of pleasure of the moment,
so blinded by desire, that they cannot foresee the
pain and trouble that are bound to ensue; and equal
blame belongs to those who fail in their duty
through weakness of will, which is the same as
saying through shrinking from toil and pain. These
cases are perfectly simple and easy to distinguish.
In a free hour, when our power of choice is
untrammeled and when nothing prevents our being
able to do what we like best, every pleasure is to
be welcomed and every pain avoided. But in certain
circumstances and owing to the claims of duty or
the obligations of business it will frequently
occur that pleasures have to be repudiated and
annoyances accepted. The wise man therefore always
holds in these matters to this principle of
selection: he rejects pleasures to secure other
greater pleasures, or else he endures pains to
avoid worse pains.
"""

def intersect_keys(d1, d2):
    assert type(d1) is dict or type(d1) is defaultdict
    assert type(d2) is dict or type(d2) is defaultdict
    ### BEGIN SOLUTION
    k1 = set(d1.keys())
    k2 = set(d2.keys())
    return k1.intersection(k2)
    ### END SOLUTION
# `intersect_keys_test`: Test cell
from random import sample

key_space = {'ape', 'baboon', 'bonobo', 'chimp', 'gorilla', 'monkey', 'orangutan'}
val_space = range(100)

for trial in range(10): # Try 10 random tests
    d1 = {k: v for k, v in zip(sample(key_space, 4), sample(val_space, 4))}
    d2 = {k: v for k, v in zip(sample(key_space, 3), sample(val_space, 3))}
    k_common = intersect_keys(d1, d2)
    for k in key_space:
        is_common = (k in k_common) and (k in d1) and (k in d2)
        is_not_common = (k not in k_common) and ((k not in d1) or (k not in d2))
        assert is_common or is_not_common
        
print("\n(Passed!)")

### BEGIN SOLUTION
english_words = get_normalized_words(english_text)
english_itemsets = make_itemsets(english_words)
english_rules = find_assoc_rules (english_itemsets, 0.75)

common_high_conf_rules = intersect_keys(latin_rules, english_rules)
### END SOLUTION

print("High-confidence rules common to _lorem ipsum_ in Latin and English:")
print_rules(common_high_conf_rules)

# `common_high_conf_rules_test`: Test cell
assert len(common_high_conf_rules) == 2
assert ('x', 'e') in common_high_conf_rules
assert ('q', 'u') in common_high_conf_rules
print("\n(Passed!)")

def on_vocareum():
    import os
    return os.path.exists('.voc')

def download(file, local_dir="", url_base=None, checksum=None):
    import os, requests, hashlib, io
    local_file = "{}{}".format(local_dir, file)
    if not os.path.exists(local_file):
        if url_base is None:
            url_base = "https://cse6040.gatech.edu/datasets/"
        url = "{}{}".format(url_base, file)
        print("Downloading: {} ...".format(url))
        r = requests.get(url)
        with open(local_file, 'wb') as f:
            f.write(r.content)            
    if checksum is not None:
        with io.open(local_file, 'rb') as f:
            body = f.read()
            body_checksum = hashlib.md5(body).hexdigest()
            assert body_checksum == checksum, \
                "Downloaded file '{}' has incorrect checksum: '{}' instead of '{}'".format(local_file,
                                                                                           body_checksum,
                                                                                           checksum)
    print("'{}' is ready!".format(file))
    
if on_vocareum():
    DATA_PATH = "../resource/asnlib/publicdata/"
else:
    DATA_PATH = ""
datasets = {'groceries.csv': '0a3d21c692be5c8ce55c93e59543dcbe'}

for filename, checksum in datasets.items():
    download(filename, local_dir=DATA_PATH, checksum=checksum)

with open('{}{}'.format(DATA_PATH, 'groceries.csv')) as fp:
    groceries_file = fp.read()
print (groceries_file[0:250] + "...\n... (etc.) ...") # Prints the first 250 characters only
print("\n(All data appears to be ready.)")

# Confidence threshold
THRESHOLD = 0.5

# Only consider rules for items appearing at least `MIN_COUNT` times.
MIN_COUNT = 10
### BEGIN SOLUTION
# Create itemsets and compute individual item counts
baskets = []
item_counts = defaultdict(int)
for basket_raw in groceries_file.split('\n'):
    itemset = set(basket_raw.split(','))
    baskets.append(itemset)
    update_item_counts(item_counts, itemset)
print("Found {} baskets.".format(len(baskets)))

# Search for an initial set of association rules
initial_basket_rules = find_assoc_rules(baskets, THRESHOLD)

# Filter those rules to exclude infrequent items
basket_rules = {}
for (a, b), v in initial_basket_rules.items():
    if item_counts[a] >= MIN_COUNT:
        basket_rules[(a, b)] = v
### END SOLUTION

### `basket_rules_test`: TEST CODE ###
print("Found {} rules whose confidence exceeds {}.".format(len(basket_rules), THRESHOLD))
print("Here they are:\n")
print_rules(basket_rules)

assert len(basket_rules) == 19
assert all([THRESHOLD <= v < 1.0 for v in basket_rules.values()])
ans_keys = [("pudding powder", "whole milk"), ("tidbits", "rolls/buns"), ("cocoa drinks", "whole milk"), ("cream", "sausage"), ("rubbing alcohol", "whole milk"), ("honey", "whole milk"), ("frozen fruits", "other vegetables"), ("cream", "other vegetables"), ("ready soups", "rolls/buns"), ("cooking chocolate", "whole milk"), ("cereals", "whole milk"), ("rice", "whole milk"), ("specialty cheese", "other vegetables"), ("baking powder", "whole milk"), ("rubbing alcohol", "butter"), ("rubbing alcohol", "citrus fruit"), ("jam", "whole milk"), ("frozen fruits", "whipped/sour cream"), ("rice", "other vegetables")]
for k in ans_keys:
    assert k in basket_rules

print("\n(Passed!)")
