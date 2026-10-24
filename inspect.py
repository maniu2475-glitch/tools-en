import io
s = io.open('tool-site/en-site/index.html', encoding='utf-8').read()
i = s.find('regex-tester')
print(s[i-600:i+700])
