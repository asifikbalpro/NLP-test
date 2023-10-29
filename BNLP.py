import re

"""This piece of code is an intellectual property of Somikoron AI"""

class Bangla_NLP:
    def __init__(self):
        """
        Initialize the Bangla_Data_Analysis class with optional parameters.

        Args:
            content (str or None): The input text data to be analyzed (default is None).
            mapper (dict or None): A dictionary used for word mapping (default is None).
            stopper (list or None): A list containing stopwords (default is None).
        """
        self.bangla_chars = ['অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'ঋ', 'এ', 'ঐ', 'ও', 'ঔ',
                    'ক', 'খ', 'গ', 'ঘ', 'ঙ', 'চ', 'ছ', 'জ', 'ঝ', 'ঞ','ট',
                    'ঠ', 'ড', 'ঢ', 'ণ', 'ত', 'থ', 'দ', 'ধ', 'ন','প', 'ফ', 'ব',
                    'ভ', 'ম', 'য', 'র', 'ল', 'শ', 'ষ', 'স','হ', 'ড়','ড়', 'ঢ়', 'য়','ৰ','ৱ'
                    'া', 'ি', 'ী', 'ু', 'ূ', 'ৃ', 'ে', 'ৈ', 'ো', 'ৌ',"্",'়','ৎ', 'ঁ', 'ং']
        self.punctuation = ['া', 'ি', 'ী', 'ু', 'ূ', 'ৃ', 'ে', 'ৈ', 'ো', 'ৌ',"্",'়','ৎ', 'ঁ', 'ং']
        ## copy peste
        self.vowelList = ['া','ি','ী','ু','ূ','ৃ','ে','ো','ৌ',"্",'়','ৎ', 'ঁ', 'ং']
        self.sufDict = {'খানি':'খানি','খানিকে' : 'খানি','খানিকেই': 'খানি','খানিকেও':'খানি','খানির':'খানি', 
            'গুলো':'গুলো','গুলোকে':'গুলো','গুলোর':'গুলো','গুলোরে': 'গুলো', 'গুলোরেই':'গুলো',
            'গুলোতে':'গুলো','গুলা':'গুলা','গুলাকে':'গুলা','গুলার':'গুলা','গুলারে':'গুলা','গুলি':'গুলি',
            'গুলারেই':'গুলা','গুলারেও':'গুলা','গুলাতে':'গুলা','গুলিকে':'গুলি','গুলির' :'গুলি',
            'গুলিরে':'গুলি','গুলিরেই':'গুলি','গুলিরেও':'গুলি','গুলিতে':'গুলি','গুলোরেও':'গুলো',
            'ভাবে':'ভাবে','ভাবেই':'ভাবে','ভাবেও':'ভাবে','ভাবের':'ভাবে','ভাবেতে':'ভাবে'
            }
        self.pList1 = [chr(32),chr(33),chr(34),chr(38),chr(39),chr(40),chr(41),chr(58),chr(63),
                    chr(91),chr(93),chr(124),chr(187),chr(2404),chr(2405),chr(8220),chr(8221),
                    chr(8730)]
        self.pList2 = ['£', '·', '»', 'Į', '৷', 'า', 'ጎ', '€', '√', '≈', 'و']

    def identifier(self, content):
        """
        Identify the data type of the given content.

        Args:
            content: The input data to be identified.

        Returns:
            type: The data type of the content.

        Note:
            This function simply returns the data type (e.g., str, list, dict) of the input content.
        """
        return type(content)
    
    def split_string(self, content, split_identifier=['-',"।",",","'",'_','"']):
        """
        Split the content based on the provided split identifier(s).

        Args:
            content (str or list): The input content to be split.
            split_identifier (str or list): The string or list of strings used for splitting.

        Returns:
            list: The split content.

        Raises:
            TypeError: If the input types are not as expected.

        Note:
            - If split_identifier is a string and content is a string, it splits content using the string.
            - If split_identifier is a list and content is a string, it splits content using each element of the list.
            - If split_identifier is a list and content is a list, it splits each string element in the list using each element of the split_identifier list.
        """
        if type(split_identifier) == str:
            if type(content) == str:
                return content.split(split_identifier)
            elif type(content) == list:
                temp = []
                for word in content:
                    if split_identifier in word:
                        temp.extend(word.split(split_identifier))
                    else:
                        temp.append(word)
                return temp
            else:
                return TypeError("Input type must be list or String")
            
        elif type(split_identifier) == list and type(content) == str:
            main_temp = [content]  # Initialize main_temp with the original content as a list
            for split in split_identifier:
                temp = []  # Initialize a temporary list for each split identifier
                for word in main_temp:
                    if split in word:
                        temp.extend(word.split(split))  # Split and extend the temp list
                    else:
                        temp.append(word)
                main_temp = temp  # Update main_temp with the results of the current split
            return main_temp
        
        elif type(split_identifier) == list and type(content) == list:
            main_temp = content.copy()  # Make a copy of the original content list
            for split in split_identifier:
                temp = []  # Initialize a temporary list for each split identifier
                for word in main_temp:
                    if isinstance(word, str) and split in word:
                        temp.extend(word.split(split))  # Split and extend the temp list
                    else:
                        temp.append(word)
                main_temp = temp  # Update main_temp with the results of the current split
            return main_temp

        else:
            raise TypeError("Split identifier must be string or character")
        

    def only_bangla(self, content):
        """
        Filter out non-Bangla words and punctuation from the content.

        Args:
            content (list): The list of words to be filtered.

        Returns:
            list: The filtered list containing only Bangla words.

        Raises:
            TypeError: If the input type is not a list.

        Note:
            - This function iterates through each word in the input list.
            - It checks if each character in a word is a Bangla character.
            - Words with at least one non-Bangla character or starting with punctuation are excluded.
        """
        if type(content) == list:
            total_list = []
            for word in content:
                ifnot = True
                for char in word:
                    if char not in self.bangla_chars:
                        ifnot = False
                if len(word) != 0 and ifnot:
                    total_list.append(word)
            return total_list
        else:
            raise TypeError("Input must be list")


    def word_mapping(self, content, map_content):
        """
        Map words in the content to their corresponding values in the map_content dictionary.

        Args:
            content (list): The list of words to be mapped.
            map_content (dict): The dictionary containing word mappings.

        Returns:
            list: The list of words with mapped values based on the map_content dictionary.

        Raises:
            TypeError: If the input types are not as expected.

        Note:
            - This function maps words in the content list to their corresponding values as defined in the map_content dictionary.
            - It checks if both content and map_content have the expected data types before proceeding.
        """
        if type(content) == list and type(map_content) == dict:
            maplist = []
            inverted_mapper = {}
            for key,values in map_content.items():
                for value in values:
                    inverted_mapper.setdefault(value, key)
            for word in content:  
                found_keys = inverted_mapper.get(word)
                if found_keys:
                    maplist.append( found_keys )
                else:
                    maplist.append(word)
            return maplist
        else:
            raise TypeError("content must be list and mapper must be dictionary")
    

    def word_stopper(self, content, stopper):
        """
        Remove stopwords from the content based on their type.

        Args:
            content (list or dict): The input content from which stopwords will be removed.
            stopper (list or dict): The list of stopwords or a dictionary containing stopwords.

        Returns:
            list or dict: The content with stopwords removed.

        Raises:
            TypeError: If the input types are not as expected.

        Note:
            - This function removes stopwords from the content based on their type (list or dict).
            - If content is a list and stopper is a list, it removes stopwords from the list.
            - If content is a dict and stopper is a list, it removes dictionary entries where keys match stopwords.
            - If content is a list and stopper is a dict, it removes list elements that match stopwords' values.
            - If content is a dict and stopper is a dict, it removes dictionary entries where keys match stopwords' values.
        """
        if type(content) == list and type(stopper) == list:
            temp = []
            for word in content:
                if word not in stopper:
                    temp.append(word)
            return temp
        elif type(content) == dict and type(stopper) == list:
            temp = {}
            for key, val in content.items():
                if key not in stopper:
                    temp[key] = val
            return temp
        elif type(content) == list and type(stopper) == dict:
            temp = []
            for word in content:
                if word not in stopper.values():
                    temp.append(word)
            return temp
        elif type(content) == dict and type(stopper) == dict:
            temp = {}
            for key, val in content.items():
                if key not in stopper.values():
                    temp[key] = val
            return temp
        else:
            raise TypeError("invalid content or stopper type[must be dict or list]")

## copy paste
    def stemming(self, content):
        """
        Apply stemming rules to the words in the content.

        Args:
            content (list): The list of words to apply stemming to.

        Returns:
            list: The list of words after applying stemming rules.

        Raises:
            TypeError: If the input type is not a list.

        Note:
            - This function applies stemming rules to the words in the content list to reduce words to their root forms.
            - It checks if the input is a list before proceeding with stemming.
            - The stemming rules include handling specific suffixes and replacements based on predefined rules.
        """
        if type(content) == list:
            temp = []
            for word in content:
                wl = len(word)
                if word.endswith('ির'):           # rule 1a
                    ind = word.rfind('ির')
                    _word = word[0:ind+1]
                    temp.append( _word )
                elif word.endswith('ীর'):         # rule 1b
                    ind = word.rfind('ীর')
                    _word = word[0:ind+1]
                    temp.append( _word )
                elif word.rfind('দের',wl-3)>0:     # rule 1c
                    _word = word[0:wl-3]
                    temp.append( _word )
                elif word.rfind('ের',wl-2)>0:     # rule 1d
                    if len(word)>3:
                        _word = word[0:wl-2]
                        temp.append( _word )
                    else:
                        temp.append(  word )
                else:
                    temp.append( word )
            temp =[x for x in temp if len(x)>1]
            temp2 = []
            for word in temp:
                for key,val in self.sufDict.items():
                    if word.endswith(key):
                        ind = word.rfind(key)
                        _word = word[0:ind]
                        if ind==0:
                            word = ''
                            break
                        elif ind==1:
                            if _word=='এ':
                                word = 'এই'
                            elif _word=='ঐ':
                                word = 'অই'
                            else:
                                word = _word+val
                            break
                        elif ind==2 and _word[1] in self.vowelList:
                            if _word=='সে':
                                word = 'সেই'
                            elif _word=='যে':
                                word = 'যেই'
                            else:
                                word = _word+val
                            break
                        else:
                            word = _word
                    else:
                        continue
                temp2.append( word )
            temp2 =[x for x in temp2 if len(x)>1]
            return temp2
        else:
            raise TypeError("Content must a list")


    def remove_lower_dots(self, wordList):
        """
        rule 1 : if 'dot' comes as the first letter
        rule 2 : if 'dot' comes as the last letter and only after vowels
        rule 3 : if 'dot' comes as redundant after রড়ঢ়য়
        rule 4 : if 'dot' comes anywhere in a word not following rule 1,2,3
    
        #re.findall(chr(2492), 'চড়থাপ্পড়')
        #[(x,ord(x)) for x in 'ডঢবয']
        #[('ড', 2465), ('ঢ', 2466), ('ব', 2476), ('য', 2479)]
        #[('ড়', 2524), ('ঢ়', 2525), ('র', 2480), ('য়', 2527)]
        """
        
        # Organization of letters in the following lists 
        # ক,খ,গ,ঘ,ঙ,চ,ছ,জ,ঝ,ঞ,
        # ট,ঠ,'ড','ঢ',ণ,
        # ত,থ,দ,ধ,ন,
        # প,ফ,'ব',ভ,ম,
        # 'য',র,ল,শ,ষ,
        # স,হ
        # '়'

        if not type(wordList) is list:
            raise TypeError("def remove_lower_dots : wordList must be a list") 

        origChar = [2453,2454,2455,2456,2457,2458,2459,2460,2461,2462,
                    2463,2464,2465,2466,2467,
                    2468,2469,2470,2471,2472,
                    2474,2475,2476,2477,2478,
                    2479,2480,2482,2486,2487,
                    2488,2489,
                    2492]
        # Check : [chr(x) for x in origChar]
        propChar = [2453,2454,2455,2456,2457,2458,2459,2460,2461,2462,
                    2463,2464,2524,2525,2467,
                    2468,2469,2470,2471,2472,
                    2474,2475,2480,2477,2478,
                    2527,2480,2482,2486,2487,
                    2488,2489,
                    32]
        # Check : [chr(x) for x in propChar]
        
        
        # Define a local list
        tmpList = []
        
        
        # Main loop begins 
        for word in wordList:
            
            if chr(2492) in word:
                dots = re.findall(chr(2492), word)
    
                for dot in dots:
                    letters =  list(word)
                    ind = letters.index( dot )
                    
                    #print(word, letters, ind)
                    
                    # rule 1 : '়','়ক',
                    if ind==0:
                        letters.pop(ind)
                        word = ''.join(letters) 
                    # print('1',word)
                    
                    # rule 2 : 'আঁকা়'
                    elif ind==len(letters)-1 and letters[ind-1] in 'ািীুূৃেৈোৌ':
                        letters.pop(ind)
                        word = ''.join(letters) 
                        #print('2',word)
                        
                    # rule 3 : 'নিয়়েই'
                    elif letters[ind-1] in 'অআইঈউঊঋএঐওঔরড়ঢ়য়':
                        letters.pop(ind)
                        word = ''.join(letters) 
                        #print('3',word)
                        
                    # rule 4 : 'নি়র্যাতিত'
                    elif ind!=len(letters)-1 and letters[ind-1] in 'ািীুূৃেৈোৌ':
                        letters.pop(ind)
                        word = ''.join(letters) 
                        #print('4',word)
                
                    # rule 5 : general case
                    else:
                        for i in range(len(origChar)):                       
                            if letters[ind-1]==chr(origChar[i]):  
                                letters[ind-1]=chr(propChar[i])
                                letters.pop(ind)
                                word = ''.join(letters) 
                        #print('5',word)
                        
                tmpList.append( word )
                
            else:
                tmpList.append( word )
            
        return tmpList

    ### unnecessary now..       
    def extra_puncts(self, content):
        if type(content) == list:
            tmpList = []
            # Add constraints 
            # Apply pList1
            for word in content:
                if len(word)>1 and word[0] in self.pList1: 
                    word = word[1:]
                elif len(word)>1 and word[-1] in self.pList1 + [chr(8217)]:
                    word = word[:-1]
                elif len(word)>1 and chr(39) in word:
                    word = re.sub(chr(39),chr(8217), word)
                elif len(word)==1 and word in self.pList1 + [chr(8217)]:
                    continue
                elif len(word)==1 and word in '০১২৩৪৫৬৭৮৯':
                    continue
                elif len(word)==1 and word in [chr(46),chr(2509)]:  #[".","্"]
                    continue
                elif len(word)==0:
                    continue
                else:
                    word = word
                tmpList.append( word.strip() )
            # Remove English words
            tmpList = [re.sub('[a-zA-Z0-9]+','',x) for x in tmpList]
            # Remove Bangla numbers
            tmpList = [re.sub('[০১২৩৪৫৬৭৮৯]','',x) for x in tmpList]
            # Remove additional punctuations
            tmpList = [re.sub('[!&@#$%=\.\(\)\{\}:><\/]','',x) for x in tmpList]
            # Apply pList2 
            tmpList =[x for x in tmpList if x not in self.pList2]
            # Remove any char like '…' = chr(8230)
            _tmpList = []
            for word in tmpList:
                if chr(8230) in word:
                    if len(word)==1:
                        continue
                    else:
                        _tmpList.append( re.sub(chr(8230),'', word) )
                else:
                    _tmpList.append(word)
            tmpList =[x for x in _tmpList if len(x)>0]
            return tmpList 
        else:
            raise TypeError("Content must a list")  

    def remove_lone_hashanta(self, content):
        """
        This piece of code is an intellectual property of Somikoron AI

        part 1: removes hashanta, chr(2509), from the end of the word
        part 2: removes hashanta, chr(2509), preceding a white space in any word
        """
        if not type(content) is list:
            raise TypeError("def lone hashanta : words must be a list") 
        # Part 1
        tmpList1 = []
        for word in content:
            if word == chr(2509):
                _word = word[:-1]
    #            _word = re.sub(chr(2509),'', word)
    #             if chr(32) in _word:
    #                 _word = re.sub('\s','', _word)
                tmpList1.append( _word )
            else:
                tmpList1.append( word )
        #print(tmpList1)
        # Part 2
        if len(tmpList1)>0:
            tmpList2 = []
            for word in tmpList1:
                if chr(32) in word:
                    ind = word.find( chr(32) )
                    if word[ind-1]==chr(2509):
                        letters = list(word)
                        letters[ind-1] = chr(32)
                        word = re.sub('\s','',''.join(letters))
                    else:
                        letters = list(word)
                        word = re.sub('\s','',''.join(letters))
                    tmpList2.append( word )
                else:
                    tmpList2.append( word )  
            return tmpList2
        else:
            return None           
        

    def Bangla_Data_Processing(self, content, mapper, stopper, split_from):
        print("Bangla_Data_Processing...")
        """
        Analyze Bengali text data by performing a series of text processing steps.

        Args:
            content (str or list): The input text data to be processed.
            mapper (dict): A dictionary used for word mapping.
            stopper (list or dict): A list or dictionary containing stopwords.
            split_from (str): The string used for splitting content.

        Returns:
            str: The processed text data after processing.

        Raises:
            TypeError: If the input types are not as expected.
        """
        # Check if content is a string, mapper is a dictionary, and stopper is a list
        if type(content) == str and type(mapper) == dict and type(stopper) == list:
            # Split the content based on split_from
            split_data = self.split_string(content, split_from)
            print("spliting complete...")
            # Extract only Bengali characters
            # only_bangla = self.only_bangla(split_data)
            # print("only bangla word are taken...")
            # Convert to lowercase and remove extra dots
            dot = self.remove_lower_dots(split_data)
            print("lower dot removed or modified...")
            # Remove extra punctuation
            punch = self.extra_puncts(dot)
            print("punchuation charecter process complete...")
            # Map words using the provided mapper
            mapping = self.word_mapping(punch, mapper)
            print("mapping complete...")
            # Apply stemming
            stem = self.stemming(mapping)
            print("stamming complete...")
            # Remove stopwords from the mapped words
            word_stopper = self.word_stopper(stem, stopper)
            print("stopper applied...")
            return word_stopper

        # Check if content is a list, mapper is a dictionary, and stopper is a list
        elif type(content) == list and type(mapper) == dict and type(stopper) == list:
            # Split the content based on split_from
            split_data = self.split_string(content, split_from)
            print("spliting complete...")
            # Extract only Bengali characters
            # only_bangla = self.only_bangla(split_data)
            # print("only bangla word are taken...")
            # Convert to lowercase and remove extra dots
            dot = self.remove_lower_dots(split_data)
            print("lower dot removed or modified...")
            # Remove extra punctuation
            punch = self.extra_puncts(dot)
            print("punchuation charecter process complete...")
            # Map words using the provided mapper
            mapping = self.word_mapping(punch, mapper)
            print("mapping complete...")
            # Apply stemming
            stem = self.stemming(mapping)
            print("stamming complete...")
            # Remove stopwords from the mapped words
            word_stopper = self.word_stopper(stem, stopper)
            print("stopper applied...")
            return word_stopper

        # Check if content is a list, mapper is a dictionary, and stopper is a dictionary
        elif type(content) == list and type(mapper) == dict and type(stopper) == dict:
            # Split the content based on split_from
            split_data = self.split_string(content, split_from)
            print("spliting complete...")
            # Extract only Bengali characters
            # only_bangla = self.only_bangla(split_data)
            # print("only bangla word are taken...")
            # Convert to lowercase and remove extra dots
            dot = self.remove_lower_dots(split_data)
            print("lower dot removed or modified...")
            # Remove extra punctuation
            punch = self.extra_puncts(dot)
            print("punchuation charecter process complete...")
            # Map words using the provided mapper
            mapping = self.word_mapping(punch, mapper)
            print("mapping complete...")
            # Apply stemming
            stem = self.stemming(mapping)
            print("stamming complete...")
            # Remove stopwords from the mapped words
            word_stopper = self.word_stopper(stem, stopper)
            print("stopper applied...")
            return word_stopper

        # Check if content is a string, mapper is a dictionary, and stopper is a dictionary
        elif type(content) == str and type(mapper) == dict and type(stopper) == dict:
            # Split the content based on split_from
            split_data = self.split_string(content, split_from)
            print("spliting complete...")
            # Extract only Bengali characters
            only_bangla = self.only_bangla(split_data)
            print("only bangla word are taken...")
            # Convert to lowercase and remove extra dots
            # dot = self.remove_lower_dots(only_bangla)
            # print("lower dot removed or modified...")
            # Remove extra punctuation
            punch = self.extra_puncts(only_bangla)
            print("punchuation charecter process complete...")
            # Map words using the provided mapper
            mapping = self.word_mapping(punch, mapper)
            print("mapping complete...")
            # Apply stemming
            stem = self.stemming(mapping)
            print("stamming complete...")
            # Remove stopwords from the mapped words
            word_stopper = self.word_stopper(stem, stopper)
            print("stopper applied...")
            
            # # Map words using the provided mapper
            # mapping = self.word_mapping(stem, mapper)
            # print("mapping complete...")   
            # # Remove stopwords from the mapped words
            # word_stopper = self.word_stopper(mapping, stopper)
            # print("stopper applied...")         
            # print("Data process complete...")
            return word_stopper
        else:
            raise TypeError("content= list or string , mapper=dictionary, stopper = list or dict")

