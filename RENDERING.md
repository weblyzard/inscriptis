## HTML rendering

The following page compares the HTML rendering obtained by 
   1. Mozilla Firefox 65
   2. inscriptis and
   3. Lynx 2.8.9dev.19
 to each other.
 
Since inscriptis is often used for natural language processing, we do not insert any line breaks, unless they are explicitley requested in the HTML code (e.g. using `<p>`, `<br>`, etc.). 
 
### Use cases

1. [Wikipedia table](#Wikipedia-table)
2. [Nested tables](#Nested-tables)
3. [Whitespace handling](#Whitespace-handling) (e.g. formatting of `<pre>` tags and `<code>` blocks)

### Wikipedia table
A table taken from the English Wikipedia page for [Chur](https://en.wikipedia.org/wiki/Chur).

* Firefox (screenshot)
<img src="https://github.com/weblyzard/inscriptis/raw/master/img/wikipedia-chur-firefox.png" align="left" alt="Wikipedia table rendered by Firefox" />

* inscriptis
```
Climate[edit]


Chur has an oceanic climate in spite of its inland position. Summers are warm and sometimes hot, normally averaging around 25 °C (77 °F) during the day, whilst winter means are around freezing, with daytime temperatures being about 5 °C (41 °F). Between 1981 and 201 Chur had an average of 104.6 days of rain per year and on average received 849 mm (33.4 in) of precipitation. The wettest month was August during which time Chur received an average of 112 mm (4.4 in) of precipitation. During this month there was precipitation for an average of 11.2 days. The driest month of the year was February with an average of 47 mm (1.9 in) of precipitation over 6.6 days.[14]

Climate data for Chur (1981-2010)
Month                                  Jan     Feb     Mar     Apr     May     Jun     Jul     Aug     Sep     Oct     Nov     Dec     Year
Average high °C (°F)                   4.8     6.4     11.2    15.1    20.0    22.7    24.9    24.1    20.0    16.1    9.5     5.3     15.0
                                       (40.6)  (43.5)  (52.2)  (59.2)  (68.0)  (72.9)  (76.8)  (75.4)  (68.0)  (61.0)  (49.1)  (41.5)  (59.0)
Daily mean °C (°F)                     0.7     1.8     5.9     9.7     14.3    17.1    19.1    18.5    14.8    10.8    5.2     1.7     10.0
                                       (33.3)  (35.2)  (42.6)  (49.5)  (57.7)  (62.8)  (66.4)  (65.3)  (58.6)  (51.4)  (41.4)  (35.1)  (50.0)
Average low °C (°F)                    −2.6    −2.0    1.6     4.6     8.9     11.8    13.8    13.7    10.3    6.6     1.7     −1.4    5.6
                                       (27.3)  (28.4)  (34.9)  (40.3)  (48.0)  (53.2)  (56.8)  (56.7)  (50.5)  (43.9)  (35.1)  (29.5)  (42.1)
Average precipitation mm (inches)      51      47      55      49      71      93      109     112     81      56      70      55      849
                                       (2.0)   (1.9)   (2.2)   (1.9)   (2.8)   (3.7)   (4.3)   (4.4)   (3.2)   (2.2)   (2.8)   (2.2)   (33.4)
Average snowfall cm (inches)           34.0    24.7    10.3    1.5     0.4     0.0     0.0     0.0     0.1     0.1     10.0    20.6    101.7
                                       (13.4)  (9.7)   (4.1)   (0.6)   (0.2)   (0.0)   (0.0)   (0.0)   (0.0)   (0.0)   (3.9)   (8.1)   (40.0)
Average precipitation days (≥ 1.0 mm)  7.3     6.6     8.1     7.5     9.9     11.2    11.0    11.2    8.4     7.0     8.5     7.9     104.6
Average snowy days (≥ 1.0 cm)          4.8     3.9     2.5     0.4     0.1     0.0     0.0     0.0     0.0     0.0     1.6     4.1     17.4
Average relative humidity (%)          73      70      65      63      64      67      68      71      73      73      74      75      70
Mean monthly sunshine hours            97      112     139     147     169     177     203     185     155     135     93      81      1,692
Source: MeteoSwiss [14]
```
* lynx
```
Climate[[166]edit]

   Chur has an [167]oceanic climate in spite of its inland position.
   Summers are warm and sometimes hot, normally averaging around 25 °C
   (77 °F) during the day, whilst winter means are around freezing, with
   daytime temperatures being about 5 °C (41 °F). Between 1981 and 201
   Chur had an average of 104.6 days of rain per year and on average
   received 849 mm (33.4 in) of [168]precipitation. The wettest month was
   August during which time Chur received an average of 112 mm (4.4 in) of
   precipitation. During this month there was precipitation for an average
   of 11.2 days. The driest month of the year was February with an average
   of 47 mm (1.9 in) of precipitation over 6.6 days.^[169][14]
   Climate data for Chur (1981-2010)
   Month Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec Year
   Average high °C (°F) 4.8
   (40.6) 6.4
   (43.5) 11.2
   (52.2) 15.1
   (59.2) 20.0
   (68.0) 22.7
   (72.9) 24.9
   (76.8) 24.1
   (75.4) 20.0
   (68.0) 16.1
   (61.0) 9.5
   (49.1) 5.3
   (41.5) 15.0
   (59.0)
   Daily mean °C (°F) 0.7
   (33.3) 1.8
   (35.2) 5.9
   (42.6) 9.7
   (49.5) 14.3
   (57.7) 17.1
   (62.8) 19.1
   (66.4) 18.5
... 
``` 

--- 

### Nested tables
A table that contains three other tables per row.

* Firefox (screenshot)
<img src="https://github.com/weblyzard/inscriptis/raw/master/img/nested-table-firefox.png" alt="Nested table rendered by Firefox" />


* inscriptis

```
 Single


First

red        green
     blue
red        green

Second

     blue       
red        green
     blue       

Nested

red        green       blue              blue       
     blue         red        green  red        green
red        green       blue              blue       
                                                    
     blue         red        green       blue       
red        green       blue         red        green
     blue         red        green       blue       
                                                    
red        green       blue              blue       
     blue         red        green  red        green
red        green       blue              blue
```

* lynx 
```
                                     Single

First

   red      green
       blue
   red      green

Second

       blue
   red      green
       blue

                                     Nested

   red      green
       blue
   red      green
       blue
   red      green
       blue
       blue
   red      green
       blue
       blue
   red      green
       blue
   red      green
       blue
   red      green
       blue
   red      green
       blue
   red      green
       blue
   red      green
       blue
   red      green
       blue
       blue
   red      green
       blue
```
### Whitespace handling

Code examples taken from [Python (programming language)](https://en.wikipedia.org/wiki/Python_(programming_language) on Wikipedia.

* Firefox (screenshot)
<img src="https://github.com/weblyzard/inscriptis/raw/master/img/wikipedia-python-example.png" align="left" alt="Python code example rendered by Mozilla Firefox" />

* inscriptis
```
  Python programming examples [ edit ]


  Hello world program:

    print('Hello, world!')
    

  Program to calculate the factorial of a positive integer:

    n = int(input('Type a number, and its factorial will be printed: '))
    
    if n < 0:
        raise ValueError('You must enter a positive integer')
    
    fact = 1
    i = 2
    while i <= n:
        fact *= i
        i += 1
    
    print(fact)
    

  Libraries [ edit ]


  Python's large standard library, commonly cited as one of its greatest strengths,[99] provides tools suited to many tasks. For Internet-facing applications, many standard formats and protocols such as MIME and HTTP are supported. It includes modules for creating graphical user interfaces, connecting to relational databases, generating pseudorandom numbers, arithmetic with arbitrary-precision decimals,[100] manipulating regular expressions, and unit testing.
```

* lynx
```
Python programming examples[edit]                                                                                                                                                                     
                                                                                                                                                                                                      
   Hello world program:                                                                                                                                                                               
                                                                                                                                                                                                      
print('Hello, world!')                                                                                                                                                                                
                                                                                                                                                                                                      
   Program to calculate the factorial of a positive integer:                                                                                                                                          
                                                                                                                                                                                                      
n = int(input('Type a number, and its factorial will be printed: '))                                                                                                                                  
                                                                                                                                                                                                      
if n < 0:                                                                                                                                                                                             
    raise ValueError('You must enter a positive integer')                                                                                                                                             
                                                                                                                                                                                                      
fact = 1                                                                                                                                                                                              
i = 2                                                                                                                                                                                                 
while i <= n:                                                                                                                                                                                         
    fact *= i                                                                                                                                                                                         
    i += 1                                                                                                                                                                                            
                                                                                                                                                                                                      
print(fact)                                                                                                                                                                                           
                                                                                                                                                                                                      
Libraries[edit]                                                                                                                                                                                       
                                                                                                                                                                                                      
   Python's large standard library, commonly cited as one of its greatest strengths,^[99] provides tools suited to many tasks. For Internet-facing applications, many standard formats and            
   protocols such as MIME and HTTP are supported. It includes modules for creating graphical user interfaces, connecting to relational databases, generating pseudorandom numbers, arithmetic         
   with arbitrary-precision decimals,^[100] manipulating regular expressions, and unit testing.                                                                                                       
```
