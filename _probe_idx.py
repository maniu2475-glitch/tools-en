s = open('index.html', encoding='utf-8').read()
k = s.find('home-card')
# print the last home-card block before the footer link area
idxs = []
p = 0
while True:
    p = s.find('home-card', p)
    if p < 0: break
    idxs.append(p); p += 1
last = idxs[-1]
first = idxs[0]
open('_probe_idx.txt', 'w', encoding='utf-8').write(
    '--- FIRST ---\n' + s[first-300:first+400] +
    '\n\n--- LAST ---\n' + s[last-300:last+500] +
    '\n\n--- MIDDLE (card 100) ---\n' + s[idxs[100]-200:idxs[100]+300])
print('ok')
