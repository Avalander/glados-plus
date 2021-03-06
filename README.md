# Extra modules for GLaDOS2

This repository contains a few extra modules designed for [GLaDOS2](https://github.com/TheComet93/GLaDOS2).

## Installation

This package can be installed using pip. Requires GLaDOS2 up and running.
```
$ pip install git+https://github.com/Avalander/glados-plus
```

## Usage

To use any of the provided modules, simply add the module to your GLaDOS2 settings.
```
# settings.json
{
	"modules": {
		"names": [
			"gladosplus.ponyfaces.Ponyfaces"
		]
	}
}
```

## Modules

### Ponyfaces

Ponyfaces wraps the http://ponyfac.es/ API into some handy commands to add ponies to your discord channel.

### Choose

Choose helps you decide by selecting a random item from a given list of choices.
```
.choose Twilight Sparkle, Pinkie Pie, Fluttershy
.choose:2 Rainbow Dash, Rarity, Applejack
```
- **.choose {choices}** Chooses one random element from `choices`.
- **.choose:{amount} {choices}** Chooses a number of random elements from `choices` equal to `amount`.
