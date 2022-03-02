import pandas as pd
import spacy

def clean(df):
    if any(df['product'].str.contains(',')): # clean all products to remove text after commas ||for example (product, 8 oz) (, 8oz) gets removed||
        ix = df[df['product'].str.contains(',')].index # this is done to optimize word embedding/parsing 
        for i in range(len(ix)):
            df.loc[ix[i], 'product'] = ','.join(df.loc[ix[i], 'product'].split(',')[:-1])
    #############################################################################
    nlp = spacy.load('en_core_web_lg') # load pretrained model & Add stop words to optimize parsing
    nlp.Defaults.stop_words |= {"2pk","3pk","4pk","5pk","6pk","7pk","8pk","9pk","10pk","11pk","12pk","14pk","20ct","5ct","6ct","B.","C","B12","%"," 1L","yd","sal","oz","cup","M", "8ct"} 
    #############################################################################
    # Create parser to extract product items "PROPN"
    # we will find the proper noun token with fewest heads as the top level proper noun
    # if no proper noun is found, we will designate `MISC`. function provided by https://github.com/ianyu93 
    def parser(x): 
        # Convert text into Doc object
        doc = nlp(x) 
        dict_ = {}
        for token in doc:
            if not token.is_stop:
                # If part-of-speech tag is not proper noun or noun, skip
                if token.pos_ in ['PROPN', 'NOUN']: 
                    # Collect length of dependencies
                    text = token.text
                    dict_[text] = []
                    source = token
                    while source.head != source :
                        dict_[text].append(source.text)
                        source = source.head
        if len(dict_) == 0: 
            return 'MISC'
        # Retrieve text with lowest dependencies
        return sorted([(k, v) for k, v in dict_.items()], key=lambda x: len(x[1]))[0][0]
    df['parsed_product'] = df['product'].apply(lambda x: parser(x)) # apply parser to each product and output result to a new column
    ##############################################
    # Manual Stemming / Cleaning
    try:
        count_edited_values = 0
        ix = df[df['parsed_product'].str.contains('Yoghurt')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Yogurt'
        ix = df[df['parsed_product'].str.contains('Yogurts')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Yogurt'
        ix = df[df['parsed_product'].str.contains('Yoyos')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Yogurt'   
        ix = df[df['parsed_product'].str.contains('Avocados')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Avocado'   
        ix = df[df['parsed_product'].str.contains('Avacado')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Avocado' 
        ix = df[df['parsed_product'].str.contains('Almonds')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Almond' 
        ix = df[df['parsed_product'].str.contains('Bagels')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Bagel' 
        ix = df[df['parsed_product'].str.contains('Lentils')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Lentil' 
        ix = df[df['parsed_product'].str.contains('Packets')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Packet' 
        ix = df[df['parsed_product'].str.contains('Sausages')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Sausage' 
        ix = df[df['parsed_product'].str.contains('Tomatoes')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Tomato' 
        ix = df[df['parsed_product'].str.contains('Tortellni')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Tortellini' 
        ix = df[df['parsed_product'].str.contains('Tortillas')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Tortilla' 
        #
        ix = df[df['category'].str.contains('supplements')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'supplement' 
            
        ix = df[df['parsed_product'].str.contains('Zolli')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Snack' 	

        ix = df[df['parsed_product'].str.contains('Zero')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Drink' 	

        ix = df[df['company'].str.contains("GT's Synergy Kombucha")].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Kombucha' 	

        ix = df[df['company'].str.contains('Kor Shots')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Juice' 

        ix = df[df['company'].str.contains('Evolution Fresh')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Juice' 

        ix = df[df['company'].str.contains('California Olive Ranch')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Oil' 

        ix = df[df['company'].str.contains('Chobani')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Yogurt' 

        ix = df[df['company'].str.contains('Vega')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'supplement' 

        ix = df[df['company'].str.contains('WTRMLN WTR')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Juice' 

        ix = df[df['parsed_product'].str.contains('Cream')][df['category'] == 'frozen_foods'].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Ice Cream' 

        ix = df[df['product'].str.contains('Bar')][df['company'] == 'KIND Snacks'].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Bars' 

        ix = df[df['parsed_product'].str.contains('Bar')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Bars' 

        ix = df[df['product'].str.contains('Milk')][df['company'] == 'So Delicious'].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Yogurt' 

        ix = df[df['company'].str.contains('La Quercia')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Bacon'

        ix = df[df['product'].str.contains('Liquid Aminos')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Sauce'	

        ix = df[df['company'].str.contains('FROMAGER D AFFINOIS')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Cheese'

        ix = df[df['company'].str.contains('Yogi')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Tea'

        ix = df[df['company'].str.contains('North Country Smokehouse')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Bacon'

        ix = df[df['company'].str.contains('Brekki')][df['product'].str.contains('Oats')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Oats' 

        ix = df[df['company'].str.contains('Celestial Seasonings')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Tea'

        ix = df[df['company'].str.contains('Kite Hill')][df['product'].str.contains('Cheese')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Cheese' 

        ix = df[df['company'].str.contains('Icelandic Provisions')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Yogurt'
        #
        ix = df[df['company'].str.contains('Steaz')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Drink'


        ix = df[df['company'].str.contains('Ca de Ambros')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Cheese'

        ix = df[df['parsed_product'].str.contains('Tagliatelle')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Pasta'

        ix = df[df['product'].str.contains('Soup')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Soup'

        ix = df[df['parsed_product'] == 'O'].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Cereal'

        ix = df[df['parsed_product'].str.contains('Cookie')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Cookies'

        ix = df[df['parsed_product'].str.contains('Discs')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Chocolate'

        ix = df[df['parsed_product'].str.contains('Disc|Chocolate')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Chocolate'

        ix = df[df['product'].str.contains('Hummus')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Hummus'

        ix = df[df['company'].str.contains('The Good Crisp Company')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Chips'

        ix = df[df['product'].str.contains('Crisps')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Crisps'

        ix = df[df['parsed_product'].str.contains('Cracker')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Crackers'
            
        ix = df[df['parsed_product'].str.contains('Cake')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Cakes'	

        ix = df[df['company'].str.contains('PUR')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Gum'

        ix = df[df['company'].str.contains('Sesmark')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Snack'

        ix = df[df['product'].str.contains('Tilapia')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Tilapia'

        ix = df[df['product'].str.contains('Shrimp')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Shrimp'
            
        ix = df[df['product'].str.contains('Sauce')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Sauce'

        ix = df[df['product'].str.contains('Shells')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Pasta'

        ix = df[df['product'].str.contains('Penne')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Pasta'

        ix = df[df['product'].str.contains('Girasoli')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Pasta'

        ix = df[df['product'].str.contains('Ravioli')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Pasta'

        ix = df[df['product'].str.contains('Mac & Cheese')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Pasta'	

        ix = df[df['product'].str.contains('Extra Virgin Olive Oil')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Oil'

        ix = df[df['product'].str.contains('Olives')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Olives'
        ix = df[df['product'].str.contains('Chicken', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Chicken'  
        ix = df[df['product'].str.contains('Turkey', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Turkey'   
        print("Cleaned " +str(count_edited_values) + " values")
        ix = df[df['product'].str.contains('Broth')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Broth'
        ix = df[df['product'].str.contains('Marinara')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Sauce'
        ix = df[df['product'].str.contains('Juice')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Juice'

        ix = df[df['product'].str.contains('Toothpaste')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Toothpaste'	
        ix = df[df['product'].str.contains('Medium Roast|Coffee|Brew')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Coffee'

        ix = df[df['parsed_product'].str.contains('soap', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Soap'

        ix = df[df['product'].str.contains('Kombucha')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Kombucha'

        ix = df[df['company'].str.contains('Essentia')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Water'

        ix = df[df['product'].str.contains('Soap')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Soap'

        ix = df[df['company'].str.contains('AURA CACIA')][df['product'].str.contains('Oil')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Essential Oil'

        ix = df[df['product'].str.contains('noodle', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Noodles'

        ix = df[df['product'].str.contains('Cavatappi|Spaghetti')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Pasta'

        ix = df[df['product'].str.contains('Potato Chip')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Chips'
        ix = df[df['product'].str.contains('Juice')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Juice'
        ix = df[df['product'].str.contains('Soup')].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Soup'
        ix = df[df['product'].str.contains('sparkling', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Seltzer'
        ix = df[df['product'].str.contains('flatbread', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Flatbread'
        ix = df[df['category'].str.contains('desserts', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Dessert'
        ix = df[df['product'].str.contains('Bread', case=True)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Bread'    
        ix = df[df['product'].str.contains('Crisps', case=True)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Chips'    
        ix = df[df['parsed_product'].str.contains('Mix', case=True)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Snack'    
        ix = df[df['product'].str.contains('wash', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Wash'    
        ix = df[df['product'].str.contains('shampoo', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Shampoo'    
        ix = df[df['product'].str.contains('lotion', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Lotion' 
        ix = df[df['product'].str.contains('Mac & Cheese', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Pasta'    
        ix = df[df['parsed_product'] == 'Mac'].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Pasta'   
        print("Cleaned " +str(count_edited_values) + " values")
        ix = df[df['product'].str.contains('chocolate', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Chocolate'
        ix = df[df['product'].str.contains('jerky', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Jerky'
        ix = df[df['product'].str.contains('Instant Oatmeal', case=True)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Oats'
        ix = df[df['parsed_product'].str.contains('Oatmeal', case=True)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Oats'
        ix = df[df['product'].str.contains('fusilli|macaroni', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Pasta'
        ix = df[df['product'].str.contains('yogurt greek', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Yogurt'

        snack_item_list = 'Chocolate, Sauce, Bars, Gum, Chips, Jerky, Cookies, Puffs, Flatbread, Bread, Hummus, Crackers, Honey, Milk, Dip, Pretzels'.split(', ')
        ix = df[df['category'] == 'snacks_chips_salsas_dips'].index
        for i in range(len(ix)):
            count_edited_values+=1
            for snack in snack_item_list:
                if df.loc[ix[i], 'parsed_product'] not in snack_item_list:
                    df.loc[ix[i], 'parsed_product'] = 'Snack'
        beauty_item_list = 'Wash, Shampoo, Conditioner, Cleanser, Balm'.split(', ')
        ix = df[df['category'] == 'beauty'].index
        for i in range(len(ix)):
            count_edited_values+=1
            for beauty in beauty_item_list:
                if df.loc[ix[i], 'parsed_product'] not in beauty_item_list:
                    df.loc[ix[i], 'parsed_product'] = 'Wash'
        beverage_item_list = 'Juice, Coffee, Tea, Kombucha, Seltzer, Water, Smoothie, Lemonade, Shake'.split(', ')
        ix = df[df['category'] == 'Beverages'].index
        for i in range(len(ix)):
            count_edited_values+=1
            for beverage in beverage_item_list:
                if df.loc[ix[i], 'parsed_product'] not in beverage_item_list:
                    df.loc[ix[i], 'parsed_product'] = 'Beverage'
        body_care_item_list = 'Wash, Essential Oil, Soap, Toothpaste, Shampoo, Lotion, Deodorant, Spray'.split(', ')
        ix = df[df['category'] == 'body_care'].index
        for i in range(len(ix)):
            count_edited_values+=1
            for body_care in body_care_item_list:
                if df.loc[ix[i], 'parsed_product'] not in body_care_item_list:
                    df.loc[ix[i], 'parsed_product'] = 'body_care'
        ix = df[df['product'].str.contains('cookies', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Cookies'
        ix = df[df['product'].str.contains('kefir', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Kefir'
        ix = df[df['product'].str.contains('coconut milk', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Milk'
        ix = df[df['product'].str.contains('Almondmilk', case=True)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Almondmilk'
        ix = df[df['product'].str.contains('Chocolate Ice Cream|Mini Chocolate Sea Salt|Chocolate Chip Cookie Dough Ice Cream|Chocolate Chip Cookie Dough Non Dairy Frozen Dessert|Swiss Chocolate Gelato|Cornflake Chocolate Chip Marshmallow Ice Cream|Peanut Butter Chocolate Cookie Crush Ice Cream|Chocolate Fudge 4-Pack', case=True)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Ice Cream'
        ix = df[df['product'].str.contains('Chicken Meatballs', case=True)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Chicken'
        ix = df[df['product'].str.contains('Cereal', case=True)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Cereal'
        pantry_item_list = 'Chocolate, Pasta, Sauce, Snack, Soup, Cheese, Oil, Cereal, Broth, Rice, Tomato, Oats, Butter, Beans, Granola, Puffs, Seasoning, Honey, Noodles, Vinegar, Olives, Noodles, Hummus, Sweetener, Paste, Spread, Dip, Flour'.split(', ')
        ix = df[df['category'] == 'pantry_essentials'].index
        for i in range(len(ix)):
            count_edited_values+=1
            for pantry in pantry_item_list:
                if df.loc[ix[i], 'parsed_product'] not in pantry_item_list:
                    df.loc[ix[i], 'parsed_product'] = 'Pantry'
        ix = df[df['product'].str.contains('Lobster Bisque|chowder|beef chili', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Soup'
        ix = df[df['product'].str.contains('Cheese|Cubes|Gouda|Cheddar|Mozzarella|Fondue|Brie|Feta|Cremeux', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Cheese'
        ix = df[df['product'].str.contains('Drink|Beverage', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Beverage'
        ix = df[df['product'].str.contains('Yogurt', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Yogurt'
        
        dairy_item_list = 'Chocolate, Beverage, Pasta, Yogurt, Cheese, Bars, Milk, Butter, Almondmilk'.split(', ')
        ix = df[df['category'] == 'dairy_eggs'].index
        for i in range(len(ix)):
            count_edited_values+=1
            for dairy in dairy_item_list:
                if df.loc[ix[i], 'parsed_product'] not in dairy_item_list:
                    df.loc[ix[i], 'parsed_product'] = 'Dairy'

        frozen_item_list = 'Chocolate, Pasta, Yogurt, Broth, Bars, Chicken, Ice Cream, Dessert, Flatbread, Bread, Gelato'.split(', ')
        ix = df[df['category'] == 'frozen_foods'].index
        for i in range(len(ix)):
            count_edited_values+=1
            for frozen in frozen_item_list:
                if df.loc[ix[i], 'parsed_product'] not in frozen_item_list:
                    df.loc[ix[i], 'parsed_product'] = 'Frozen'

        meat_item_list = 'Chicken, Salami, Bacon, Turkey, Ham, Pork, Steak, Bison, Lamb, Beef, Sausage, Ribs'.split(', ')
        ix = df[df['category'] == 'meat'].index
        for i in range(len(ix)):
            count_edited_values+=1
            for meat in meat_item_list:
                if df.loc[ix[i], 'parsed_product'] not in meat_item_list:
                    df.loc[ix[i], 'parsed_product'] = 'Meat'
        ix = df[df['category'].str.contains('Produce', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Produce'
        ix = df[df['category'].str.contains('seafood', case=False)].index
        for i in range(len(ix)):
            count_edited_values += 1
            df.loc[ix[i], 'parsed_product'] = 'Seafood'
            

    except Exception as e:
        print(e)
        print("Cleaned " +str(count_edited_values) + " values")