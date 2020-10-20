from bs4 import BeautifulSoup

soup = BeautifulSoup(open("./src/crawling.html", encoding='utf-8'), "html.parser")

li_tag = soup.select('li')

result_text = []

for tag in li_tag:

    em = tag.select('em')
    for extract_tag in em:
        extract_tag.extract()

    # span = tag.select('span')
    # for extract_tag in span:
    #     extract_tag.extract()

    result_text.append(tag.getText().strip())

print(result_text)