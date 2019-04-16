my_text = ['1', '-1.0', 'garbage', 13]

for word in my_text:
    try:
        int(word)
    except ValueError:
        print('{} is not able to become an int'.format(word))
    else:
        print('{} is now an integer'.format(word))

aa = 3
bb = 4
cc = 12

if cc < (aa * bb):
    print("Allowed")
else:
    print("Not Allowed")
