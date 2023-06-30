import json
import time
from bs4 import BeautifulSoup
import requests
import selenium
from selenium.webdriver.support.select import Select
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException

import itertools
from pprint import pformat


string='color:red,blue /   size:12,13'
input_dict = dict(item.strip() .split(':') for item in string.split('/'))
js=json.dumps(input_dict)
print(js)

# driver = Chrome()
# driver.get('https://www.ebay.com/itm/364173634929?_trkparms=amclksrc%3DITM%26aid%3D1110006%26algo%3DHOMESPLICE.SIM%26ao%3D1%26asc%3D250629%26meid%3D6f0a7449bb40433d9c3abd9c86c65b89%26pid%3D101195%26rk%3D2%26rkt%3D12%26sd%3D185952869279%26itm%3D364173634929%26pmt%3D1%26noa%3D0%26pg%3D2047675%26algv%3DSimplAMLv11WebTrimmedV3MskuWithLambda85KnnRecallV1V4V6ItemNrtInQueryAndCassiniVisualRankerAndBertRecallAndPBoosterV3a%26brand%3DApple&_trksid=p2047675.c101195.m1851&amdata=cksum%3A3641736349296f0a7449bb40433d9c3abd9c86c65b89%7Cenc%3AAQAIAAABUOF2C1v4PvLuUMt94LTx3USaOPJBiGrcV6%252Fms53nuTmrZ3dyQNOibl5UuvBUL5wYmcuhlieo3faZqx%252BhFc6Ti9XirkkCUJ2LfxVb%252B9nxabunfUYGsMpL1Y%252FxmkjPHNCqMgXo2ECai9wWaAOy6fJOFjRG8Y6EIR%252BV10H7oSEAFZzjirEo6xzjrj6pvQuDsEgW%252FGcDUVLtKZLSIxhFeGH1QI0OLCBY1qrXCss%252BWBT8UWa%252B9o7UmKZW9NaArsxfhRmWrTLtV8lzsRznrL0FjUOqbX4GQOXtHLr1zaT9NC1rwmQ99jRYAj25QBX%252FSymPmPGIGQaKhS%252F2croQCvm%252FmAbTGJwhy6GMII6g00TM%252FVILVvKAFcSbvccv3%252B0Iy2iDCkOJjwLDPZWAjZKsAslUBxB381De2go%252F%252FGeIRzu8S6kc3x5CBkCkKV4Vo9Nrxpoc7jD7bw%253D%253D%7Campid%3APL_CLK%7Cclp%3A2047675')
# els = driver.find_elements("css selector", '.x-msku')
# els = driver.find_elements('class name','x-msku__select-box')



# selects = []
# for el in els:
#     # Adding the dropdown name to the select object
#     name = el.get_attribute('selectboxlabel')
#     select = Select(el)
#     select.name = name
#     selects.append(select)


# #print("Get all options for each dropdown")
# for idx, sel in enumerate(selects):
#     sel.values = [option.text for option in sel.options][1:]
#     print(sel.values)
# string_data = "\"rom\":\"128 GB\",\"coulor\":\"Blue,Starlight\""
# formatted_string = '{' + string_data + '}'
# dictionary = json.loads(formatted_string)
# len_options = len(dictionary)
# li=list(value.split(',') for key, value in dictionary.items())
# permutations = list(itertools.product(*li))
# permutations=[('Silver', '512GB')]
# # print('permutations',permutations)
# #print("Get all possible permutations")
# #permutations = list(itertools.product(*[ sel.values for sel in selects ]))
# #permutations = list(itertools.product(*[ sel.values for sel in selects ]))
# #permutations=[('128 GB','Blue')]

# #print(permutations)

# # permutations=[li]

# # Iteration for all possible permutation
# print("Select all possible permutation and get price for each")
# results = []
# for permutation in permutations:
#     # Resetting all parameter to default
#     for sel in selects:
#         try:
#             sel.select_by_index(0)
#         except Exception as e:
#             print(e)
#             pass
        
#     # Iteration to set each dropdown
#     result = apply_values(selects, permutation)
#     if result:
#         # Once all dropdown value are set, get the finally price
#         time.sleep(1)
#         result['Price'] = driver.find_element("css selector", ".x-price-primary").find_element("css selector", 'span[itemprop="price"]').get_attribute('content')#driver.find_element_by_id("prcIsum").text
#         if len(result) == len_options +1:
#             results.append(result)


# list_item=results
# min_item= min(list_item, key=lambda x: float(x['Price']))
# print(min_item['Price'])
# min_item.pop('Price')
# result = ', '.join([f"{key}: {value}" for key, value in min_item.items()])
# print(result)
# driver.close()