import pandas as pd
from datetime import date 
import pickle 
#------------------------------##------------------------------##------------------------------##------------------------------##------------------------------##------------------------------#
path = (r"C:\Users\water\Desktop\WF\WholeFoods-Datascraping-Project-Deployment\Deployment\scraped products dump\list_of_items_" + str(date.today().strftime("%b_%d_%Y")) + ".pkl")
with open(path, 'rb') as handle: # loads our saved .pkl back into a variable
  list_of_items = pickle.load(handle) 
class wholefoods_clean:
    def cleaner(self):
        d = {"company":[], "product":[], "regular":[], "sale":[], "prime":[]} # Create a Dict

        for i in range(len(list_of_items)):                        # At the range of the length of all items (will loop i times)
                d["company"].append(list_of_items[i][-5])      # Append respective indexed data in list_of_items[i] for each column
                d["product"].append(list_of_items[i][-4])      # | -
                d["regular"].append(list_of_items[i][-3][8:])  # | * 
                d["sale"].append(list_of_items[i][-2][10:])    # | /
                d["prime"].append(list_of_items[i][-1][18:])   # | \
        #------------------------------------------------------# | /
        if len(d['company']) == len(d['product']) == len(d['regular']) == len(d['sale']):  # Verify that the length of each column is == to each other, otherwise the dataframe wont be populated   
            print("All column lengths are equal, there are " + str(len(d['company'])) + " products for sale today.")
        else:                                                  # | \        
            print("Error, column lengths are not equal.")      # | /
        pd.set_option("display.max_rows", 500)                 # | \ Change Pandas option to view more rows of the df
        df = pd.DataFrame.from_dict(d)                         # | / Turn our Dict to a Pandas DataFrame  

        # BAKERY is not a product name, WholeFoods sometimes lists the origin as the product name since it is made in house
        # Because of this we will grab the indices where this is True and remove all rows that pertain to these indices
        # We will then create a new dictionary and re-append all items again with shifted index values to properly fit each KEY and Value (Ex. Bakery goes under Company in this case)
        # We will then set this new dict as df2, and reinstantiate df2 as df2 where 'BAKERY' only exists 
        # Finally we concat the df where we dropped the rows, and the new df2 that has our new 'BAKERY' rows
        if any(list(df['product'].str.contains('BAKERY'))):        
            ix = df[df['product'].str.contains('BAKERY')].index
            df = df.drop(list(ix))
            a = {"company":[], "product":[], "regular":[], "sale":[], "prime":[]}
            for i in range(len(list_of_items)):                        
                a["company"].append(list_of_items[i][-4])
                a["product"].append(list_of_items[i][-3])
                a["regular"].append(list_of_items[i][-2][8:])
                a["sale"].append(list_of_items[i][-2][8:])
                a["prime"].append(list_of_items[i][-1][19:])
            df2 = pd.DataFrame.from_dict(a)
            df2 = df2[df2['company'].str.contains('BAKERY')]
            df = pd.concat([df,df2]).sort_index()
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
        # We then sort by index and remove all '$' and '/lb' symbols from each column to prepare the data for numerical values
        df = df.sort_index()  
        df['sale'] = df['sale'].str.replace(r'$', '')
        df['prime'] = df['prime'].str.replace(r'$', '')
        df['regular'] = df['regular'].str.replace(r'$', '')
        df['sale'] = df['sale'].str.rstrip('  /lb')
        df['prime'] = df['prime'].str.rstrip('  /lb')
        df['regular'] = df['regular'].str.rstrip('  /lb')

        if any(list(df['product'].str.contains('Original Vegan Bagels, 15.87 oz'))):                         
            ix = df[df['product'].str.contains('Original Vegan Bagels, 15.87 oz')].index
            for i in range(len(ix)):
                df.loc[ix[i],'company'] = "Soozy's"
        if any(list(df['product'].str.contains('Original Sandwich Bread, 22.2 oz'))):                         
            ix = df[df['product'].str.contains('Original Sandwich Bread, 22.2 oz')].index
            for i in range(len(ix)):
                df.loc[ix[i],'company'] = "Soozy's"
        if any(list(df['product'].str.contains('Arctic Char Fillet'))):                         
            ix = df[df['product'].str.contains('Arctic Char Fillet')].index
            for i in range(len(ix)):
                df.loc[ix[i],'company'] = "Whole Foods Market"

        # Data cleaning/shifting for products by Brita
        if any(list(df['company'].str.contains('/'))) and any(list(df['product'].str.contains('Brita'))):
            ix = df[df['company'].str.contains('/')][df['product'].str.contains('Brita')].index
            for i in range(len(ix)):
                df.loc[ix[i], 'company'] = df.loc[ix[i], 'product']
                df.loc[ix[i], 'product'] = list_of_items[ix[i]][-3]
                df.loc[ix[i], 'regular'] = list_of_items[ix[i]][-2][8:]
                df.loc[ix[i], 'sale'] = 0

        # Data cleaning/shifting for products
        if any(list(df['product'].str.contains("Easy Peel White Shrimp 8-12 Count"))):
            ix = df[df['product'].str.contains("Easy Peel White Shrimp 8-12 Count")].index
            for i in range(len(ix)):
                df.loc[ix[i],'company'] = "Whole Foods Market"
        if any(list(df['product'].str.contains("Organic Freeze Dried Chives, 0.14 oz"))):
            ix = df[df['product'].str.contains("Organic Freeze Dried Chives, 0.14 oz")].index
            for i in range(len(ix)):
                df.loc[ix[i],'company'] = "Green Garden"
        if any(list(df['product'].str.contains("Organic Freeze Dried Thyme, 0.26 oz"))):
            ix = df[df['product'].str.contains("Organic Freeze Dried Thyme, 0.26 oz")].index
            for i in range(len(ix)):
                df.loc[ix[i],'company'] = "Green Garden"
        if any(list(df['product'].str.contains("Organic Mild Plant Taco Meatless Crumbles"))):
            ix = df[df['product'].str.contains("Organic Mild Plant Taco Meatless Crumbles")].index
            for i in range(len(ix)):
                df.loc[ix[i],'company'] = "PLANT BOSS"
        if any(list(df['product'].str.contains("Organic Multicolor Kale"))):
            ix = df[df['product'].str.contains("Organic Multicolor Kale")].index
            for i in range(len(ix)):
                df.loc[ix[i],'company'] = "Whole Foods Market"        

        # Data cleaning/shifting for products by Soozy's
        if any(list(df['product'].str.contains("Soozy's Birthday Cake Cookies"))):
            ix = df[df['product'].str.contains("Soozy's Birthday Cake Cookies")].index
            for i in range(len(ix)):
                df.loc[ix[i],'company'] = "Soozy's"
        if any(list(df['product'].str.contains("Soozys Chocolate Chip Cookies"))):
            ix = df[df['product'].str.contains("Soozys Chocolate Chip Cookies")].index
            for i in range(len(ix)):
                df.loc[ix[i],'company'] = "Soozy's"

        # Data cleaning/shifting for products by Whole Foods Market
        if any(list(df['product'].str.contains('Whole Foods Market'))):
            ix = df[df['product'].str.contains('Whole Foods Market')].index
            for i in range(len(ix)):
                df.loc[ix[i], 'company'] = df.loc[ix[i], 'product']
                df.loc[ix[i], 'product'] = list_of_items[ix[i]][-3]
                df.loc[ix[i], 'regular'] = list_of_items[ix[i]][-2][8:]
                df['sale'] = df['sale'].str.rstrip('  /lb')
                df['prime'] = df['prime'].str.rstrip('  /lb')
                df['regular'] = df['regular'].str.rstrip('  /lb')
                df.loc[ix[i], 'sale'] = 0

        # Data cleaning/shifting for products by CAMELBAK
        if any(list(df['product'].str.contains('CAMELBAK'))):
            ix = df[df['product'].str.contains('CAMELBAK')].index
            for i in range(len(ix)):
                df.loc[ix[i], 'company'] = df.loc[ix[i], 'product']
                df.loc[ix[i], 'product'] = list_of_items[ix[i]][-3]
                df.loc[ix[i], 'regular'] = list_of_items[ix[i]][-2][8:]
                df.loc[ix[i], 'sale'] = 0

        # Data cleaning/shifting for products by NEW WAVE
        if any(list(df['product'].str.contains('NEW WAVE'))):
            ix = df[df['product'].str.contains('NEW WAVE')].index
            for i in range(len(ix)):
                df.loc[ix[i], 'company'] = df.loc[ix[i], 'product']
                df.loc[ix[i], 'product'] = list_of_items[ix[i]][-3]
                df.loc[ix[i], 'regular'] = list_of_items[ix[i]][-2][8:]
                df.loc[ix[i], 'sale'] = 0

        # Data cleaning/shifting for products by Enviro
        if any(list(df['product'].str.contains('Enviro'))):
            ix = df[df['product'].str.contains('Enviro')].index
            for i in range(len(ix)):
                df.loc[ix[i], 'company'] = df.loc[ix[i], 'product']
                df.loc[ix[i], 'product'] = list_of_items[ix[i]][-3]
                df.loc[ix[i], 'regular'] = list_of_items[ix[i]][-2][8:]
                df.loc[ix[i], 'sale'] = 0

        # Data cleaning/shifting for products by HYDRO FLASK
        if any(list(df['product'].str.contains('HYDRO FLASK'))):
            ix = df[df['product'].str.contains('HYDRO FLASK')].index
            for i in range(len(ix)):
                df.loc[ix[i],'company'] = df.loc[ix[i], 'product']
                df.loc[ix[i],'product'] = list_of_items[ix[i]][-3]
                df.loc[ix[i], 'regular'] = list_of_items[ix[i]][-2][8:]
                df.loc[ix[i], 'sale'] = 0

        # Data cleaning/shifting for products by SUNDESA
        if any(list(df['product'].str.contains('SUNDESA'))):
            ix = df[df['product'].str.contains('SUNDESA')].index
            for i in range(len(ix)):
                df.loc[ix[i],'company'] = df.loc[ix[i], 'product']
                df.loc[ix[i],'product'] = df.loc[ix[i], 'regular']
                df.loc[ix[i], 'regular'] = list_of_items[ix[i]][-2][8:]
                df.loc[ix[i], 'sale'] = 0

        if any(list(df['product'].str.contains('Lemonade Electrolyte Powder Packet, 0.12 oz'))):
            ix = df[df['product'].str.contains('Lemonade Electrolyte Powder Packet, 0.12 oz')].index
            for i in range(len(ix)):
                df.loc[ix[i], 'regular'] = list_of_items[ix[i]][-3][7:]
        if any(list(df['product'].str.contains('Wild Raspberry Electrolyte Powder Packet, 0.11 oz'))):
            ix = df[df['product'].str.contains('Wild Raspberry Electrolyte Powder Packet, 0.11 oz')].index
            for i in range(len(ix)):
                df.loc[ix[i], 'regular'] = list_of_items[ix[i]][-3][7:]
        if any(list(df['product'].str.contains('Orange Pkt, 0.3 oz'))):
            ix = df[df['product'].str.contains('Orange Pkt, 0.3 oz')].index
            for i in range(len(ix)):
                df.loc[ix[i], 'regular'] = list_of_items[ix[i]][-3][7:]

        if any(list(df['company'].str.contains('365'))):
            ix = df[df['company'].str.contains('365')].index
            for i in range(len(ix)):
                df.loc[ix[i], 'company'] = 'Whole Foods Market'

        d = df.to_dict('list') # Take our cleaned dataframe and convert it to a dictionary for more cleaning

        for i in range(len(d['sale'])):                                                
            if isinstance(d['sale'][i], str) and 'for' in d['sale'][i].split():  
                d['sale'][i] = float(d['sale'][i].split()[2]) / float(d['sale'][i].split()[0])

        for i in range(len(d['prime'])):                                                
                if isinstance(d['prime'][i], str) and 'for' in d['prime'][i].split():  
                    d['prime'][i] = float(d['prime'][i].split()[2]) / float(d['prime'][i].split()[0])

        df = pd.DataFrame.from_dict(d) # turn our dict back into a dataframe

        df = df.fillna(0) # Sometimes NaN Values are created in Sale Price since there is no Sale Price, We also instantiate 0's here originally when there are no Sale Prices
                        # Some aggregate functions create NaN's again, so we replace them again with 0
                        # We check to see if there are any NaN values

        for i in range(len(df[df['sale'].str.contains('¢', na=False)].index)): # Append a '.' to all values that have a cents symbol
            ix = df[df['sale'].str.contains('¢', na=False)].index
            df.loc[ix[i]][3] = '.' + df.loc[ix[i]][3]

        for i in range(len(ix)):
            ix = df[df['prime'].str.contains('¢', na=False)].index
            df.loc[ix[i]][4] = '.' + df.loc[ix[i]][4]

        try:
            for i in range(len(ix)):
                ix = df[df['regular'].str.contains('¢', na=False)].index
                df.loc[ix[i]][2] = '.' + df.loc[ix[i]][2]
        except:
            pass

        ix = df[df['prime'].str.contains('¢', na=False)].index
        for i in range(len(ix)):
            df.loc[ix[i]][4] = df.loc[ix[i]][4].replace('¢', '')

        ix = df[df['regular'].str.contains('¢', na=False)].index
        for i in range(len(ix)):
            df.loc[ix[i]][2] = df.loc[ix[i]][2].replace('¢', '')

        ix = df[df['sale'].str.contains('¢', na=False)].index
        for i in range(len(ix)):
            df.loc[ix[i]][3] = df.loc[ix[i]][3].replace('¢', '')

        df["regular"] = pd.to_numeric(df["regular"]) # change columns to numeric for visualization
        df["sale"] = pd.to_numeric(df["sale"])
        df["prime"] = pd.to_numeric(df["prime"])
        df['sale_discount'] = 1-df['sale']/df['regular'] # create new feature to show percentage discount of sale price
        df['prime_discount'] = 1-df['prime']/df['regular'] # create new feature to show percentage discount of prime price
        df['prime_sale_difference'] = df['prime_discount'] - df['sale_discount'] # create new feature to show the difference between sale discount and prime discount
        df['discount_bins'] = pd.cut(df.prime_discount, [0,.25,.50,.75, 1], labels=['0% to 25%', '25% to 50%', '50% to 75%', '75% or more'])
        df = df.sort_values(by='prime_discount', ascending=False) # sort by difference
        self.df = df


#------------------------------##------------------------------##------------------------------##------------------------------##------------------------------##------------------------------#

