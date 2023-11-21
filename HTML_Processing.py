!if ! test -f yelp.htm ; then echo "...Downloading 'yelp.htm' ..." ; curl -O https://cse6040.gatech.edu/datasets/yelp-example/yelp.htm ; fi
!if ! test x"`md5sum yelp.htm | awk '{print $1;}'`" = x"4a74a0ee9cefee773e76a22a52d45a8e" ; then echo "*** Downloaded file may be corrupt; please re-run this cell. ***" ; rm -f yelp.htm ; else echo "=== File 'yelp.htm' is available locally and appears to be ready for use. ===" ; fi

with open('yelp.htm') as yelp_file:
    yelp_html = yelp_file.read()
    
# Print first few hundred characters of this string:
print("*** type(yelp_html) == {} ***".format(type(yelp_html)))
n = 1000
print("*** Contents (first {} characters) ***\n{} ...".format(n, yelp_html[:n]))

matchers = {
    'name': '''<a class="biz-name js-analytics-click" data-analytics-label="biz-name" href="[^"]*" data-hovercard-id="[^"]*"><span>(.+)</span></a>''',
    'stars': '''title="([0-9.]+) star rating"''',
    'numrevs': '''(\d+) reviews''',
    'price': '''<span class="business-attribute price-range">(\$+)</span>'''
}

def get_field(s, key):
    from re import search
    assert key in matchers
    match = search(matchers[key], s)
    if match is not None:
        return match.groups()[0]
    return None

sections = yelp_html.split('<span class="indexed-biz-name">')
rankings = []
for i, section in enumerate(sections[1:]):
    rankings.append({})
    for key in matchers.keys():
        rankings[i][key] = get_field(section, key)
    
for r in rankings:
    r['numrevs'] = int(r['numrevs'])


assert type(rankings) is list, "`rankings` must be a list"
assert all([type(r) is dict for r in rankings]), "All `rankings[i]` must be dictionaries"

print("=== Rankings ===")
for i, r in enumerate(rankings):
    print("{}. {} ({}): {} stars based on {} reviews".format(i+1,
                                                             r['name'],
                                                             r['price'],
                                                             r['stars'],
                                                             r['numrevs']))

assert rankings[0] == {'numrevs': 549, 'name': 'Gus’s World Famous Fried Chicken', 'stars': '4.0', 'price': '$$'}
assert rankings[1] == {'numrevs': 1777, 'name': 'South City Kitchen - Midtown', 'stars': '4.5', 'price': '$$'}
assert rankings[2] == {'numrevs': 2241, 'name': 'Mary Mac’s Tea Room', 'stars': '4.0', 'price': '$$'}
assert rankings[3] == {'numrevs': 481, 'name': 'Busy Bee Cafe', 'stars': '4.0', 'price': '$$'}
assert rankings[4] == {'numrevs': 108, 'name': 'Richards’ Southern Fried', 'stars': '4.0', 'price': '$$'}
assert rankings[5] == {'numrevs': 93, 'name': 'Greens &amp; Gravy', 'stars': '3.5', 'price': '$$'}
assert rankings[6] == {'numrevs': 350, 'name': 'Colonnade Restaurant', 'stars': '4.0', 'price': '$$'}
assert rankings[7] == {'numrevs': 248, 'name': 'South City Kitchen Buckhead', 'stars': '4.5', 'price': '$$'}
assert rankings[8] == {'numrevs': 1558, 'name': 'Poor Calvin’s', 'stars': '4.5', 'price': '$$'}
assert rankings[9] == {'numrevs': 67, 'name': 'Rock’s Chicken &amp; Fries', 'stars': '4.0', 'price': '$'}

print("\n(Passed!)")
