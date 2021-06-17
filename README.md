# pokerevo-set_ocr

Python app that converts a screenshot of your pokemon card from [Pokemon Revolution](https://pokemonrevolution.net/home) and returns the Pokemon in Showdown format. It can take multiple screenshot at the same time.

For constant good result it is best to have the same area snipped, I advise you to use snipping app like [Greenshot](https://getgreenshot.org/) or [Shutter](https://shutter-project.org/) which offers the option to snip the same/fixed area.

The app was done very quickly and was not optimized, it was done for a friend and I thought someone else could need it.

## Installation and Requirements

To install just clone the repo or dezip the [zip file](https://github.com/kwiikwik/pokerevo-set_ocr/archive/refs/heads/main.zip). You of course need python, at least the 3.6, you can download  [here](https://www.python.org/downloads/) the 3.9 if you don't have it (don't forget to add it to the PATH).
It uses a few modules:

- `pandas`
- `opencv-python`
- `easyocr`
- `pyperclip`
- `pynput`

You can either install them one by one by writing `pip install MODULE` or write in your shell from the root of the repo

```shell
pip install -r requirements.txt
```

If you have a CUDA GPU (check [here](https://developer.nvidia.com/cuda-gpus)) install first torch and torchvision by following the instruction [here](https://pytorch.org/get-started/locally/). Use the latest CUDA version and chose the Pip package. I strongly advise you to do so since using the GPU gives much faster results, check the [Time results 
](#time-results) section

## Usage

### Start

To start `pokerevo-set_ocr` open `pokerevo-set_ocr.py` with python or type in your terminal from the repo

```
python pokerevo-set_ocr.py
```

### Calibrate

The first thing you need to do after opening is calibrate the cropping, to do so you need to click on the button `Calibrate`, you then choose a screenshot of a Pokemon card, and select in that order:

1. Name of Pokemon
2. Ability and nature
3. Moves without the 'Moves' title
4. The last two rows of stats (just IVs and EVs)

![calibrate](/gifs/calibrate.gif)

You don't need to do that step everytime, once you did it and your screenshots are around the same size you don't have to do it more. That is why I strongly advise the use of [Greenshot](https://getgreenshot.org/) or [Shutter](https://shutter-project.org/).

### Convert

To convert your Pokemon you just need to click on `Choose File` at the top, then choose the screenshots of the Pokemon cards you want to convert then click on the `Convert` button. You can convert multiple Pokemon card at the same time, it takes around 3~4 sec to convert per Pokemon

![convert](/gifs/convert.gif)

You then can either copy the sets to the clipboard by clicking on `Copy` or create a `set.txt` file at the root containing the set by clicking the `set.txt` button.

If the window doesn't respond it doesn't mean there is an error it is just working behind, in case of an error the window will work normally but won't return anything and you'll see an error in the terminal. In that case usually it's either a faulty cropping or a misreading of the cropped screenshots, to see what the issue might be I suggest you to turn the checkboxes

- `Create cropped screenshots` : it will create at the root the 3 framed that you took during the calibration
- `Print text read from screenshots` : it will print in the terminal what the ocr recognized from the cropped screenshots

You can use them to see whether your calibration was wrong or it's simply an issue with the ocr and you can't really do anything about it  ¯\\_(ツ)_/¯

It's better to have the path of the files you select to not contain characters with accents and spaces since it might cause an error.

## Limitation of program

While there won't be any issue —if the calibration is well done— with the recognition of the name, moves, nature and ability since I can compare it to a database, there might be some issues with the recognition of the IVs and EVs, in this case either the program won't return anything or it might just give the wrong number for some stats. 

## Time results

Results in second from 130 convertions:

|         | CPU: i5-4300U @ 2.9GHz | CPU: i5-7300HQ @ 2.5GHz | GPU: Geforce GTX 1060 |
| :-----: | :--------------------: | :---------------------: | :-------------------: |
| Average |   2.8847809519086565   |   1.5021841620144092    |   0.352505401464609   |
| Median  |   3.9633853435516357   |    1.502927303314209    |  0.34704041481018066  |