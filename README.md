# Terraria Game Wiki Scraper :rabbit2:

This is a simple script that should be paired with the single page app, Terraria Classes Guide ([GitHub repo](https://github.com/mbgeorge48/terraria_classes))

## Setup

_The setup for this script isn't strict so feel free to setup the way you normally would. otherwise..._

1. Create your virtual env

```
python3 -m venv env
```

| Unix                      | Windows                    |
| ------------------------- | -------------------------- |
| `source env/bin/activate` | `env\Scripts\activate.bat` |

2. Install any requirements

```
pip install -r requirements.txt
```

3. Run the script

```
python game-wiki-scraper.py
```

## Example Output

The output is an array of JSON objects that follow this rough format:

```json
[
  {
    "name": "Gold Bow",
    "url": "https://terraria.fandom.com/wiki/wiki/Gold_Bow",
    "imgPath": "https://static.wikia.nocookie.net/terraria_gamepedia/images/f/ff/Gold_Bow.png",
    "role": "ranged",
    "category": "weapons",
    "gameStageAvailable": 0
  }
]
```

### Scraping Details

Move items are found by traversing the HTML and looking for this section of elements:

```html
<span style="xyz" class="abc">
  <a href="url" title="Item Name">
    <img alt="Item Name" src="img path" data-src="img path" ... />
  </a>
  <span>
    <span>
      <a href="url" title="Item Name"> Item Name </a>
    </span>
  </span>
</span>
```

From the above `span` you can find the `name` and `imgPath`, the `url` can be derived using the base url and the url found in the `a` tags

The `role`, `category` and `gameStageAvailable` are found from the parent containers

Sometimes items appear in the HTML as:

```html
<li style="xyz">
  <span class="abc">
    <a href="url" title="Item Name">
      <img alt="Item Name" src="img path" data-src="img path" class="abc" />
    </a>
    <span>
      <span>
        <a href="url" title="Item Name ">Item Name</a>
      </span>
    </span>
  </span>
</li>
```

However the data can be extracted in quite a simular way

#### Known Issues / Future Features

When extracting the `imgPath` there are two `attributes` that contain the path. `img.src` and `img.data-src`. I haven't fully explored it yet however sometimes both, one or none of those contain an encoded path which I'm unable to use.
