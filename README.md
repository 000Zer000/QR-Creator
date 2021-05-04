# QR-creator
A python script which allows you to generate QR-codes, Any kind at ANY SIZE

## Features

1. More than 10 output formats:
   
    1. bmp
       
    2. ico
       
    3. jpeg
       
    4. png
       
    5. webp
        
    Plus many other which are supported but not listed here
       
2. Easy to use
   
3. Also powerful
   
4. Hate the black color ? You pick the color!

Want to have it ? Let's go for installation, don't worry it will be pretty easy

## Installing

Simply clone the repo:

```shell
git clone https://github.com/TheOddZer0/QR-Creator
```
Then install with pip:
```shell
pip install .
```

## Usage

simply run `qr-creator`, This script also allows for customization, Let's take a look at help banner:

```text 
  -h, --help            show this help message and exit
  --fore-color FORE_COLOR, -fc FORE_COLOR Which color to use as the foreground color, defaults to 'black'
  
  --back-color BACK_COLOR, -bc BACK_COLOR Which color to use as the background color, defaults to 'white'
  
  --border BORDER, -b BORDER Increase or decrease the thickness of border, defaults to '4' and cannot be lower then
  
  --input INPUT, -in INPUT Instead of reading from STDIN, Read the content of the file
  
  --size SIZE, -s SIZE  Increase the size, defaults to whatever suits your data, the biggest is 40
  
  --output OUTPUT, -o OUTPUT Which file to store output as, defaults to 'Output'
  
  --kind KIND, -k KIND  What kind of picture do you want, defaults to 'png'
```
You can simply make a QR code with red foreground by this:
```shell
python creator.py -fc red
```

So You can easily play with the flags to generate your own QR code

## Contacting me

You can reach me by emailing me (`TheOddZer0@protonmail.com`)

## License

This repo is licensed under Apache 2.0, Read [COPYING](https://github.com/TheOddZer0/QR-Creator/blob/main/COPYING) file for more info
