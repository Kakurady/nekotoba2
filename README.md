A handwriting font I started to make in 2011. Drew characters in Inkscape using Wacom tablet and imported them into Fontforge. 

Covers ASCII and a few smattering of punctuations and symbols, and intending to cover all [HSK list of characters](https://en.wiktionary.org/wiki/Appendix:HSK_list_of_Mandarin_words) and eventually all of [GB 2312](https://en.wikipedia.org/wiki/GB_2312). 

The effort fizzled out because converting from Inkscape's Beizer curves to .ttf cubic Beizer curves for thousands of character is too time consuming, especially when Fontforge keeps complaining "Confusion wiggles!" repeatedly. ([I'm not kidding about "Confusion wiggles!", it's a real error in Fontforge.](https://github.com/fontforge/fontforge/blob/decc0dcb803206e99910ba1331573d568222d40c/fontforge/splinestroke.c#L3151-L3154))

And now I am hesitant to add new characters because I forgot the Inkscape settings I used. It's still the most legible font I made, but the kerning is not perfect, so I'd sometimes need to adjust it. 

## Principles ##
- Display font suitable for comics, games, and titling your blog posts (actually really bad because of small x-height)
- Give CJK characters variable width. Chinese "block characters" is a limitation of movable type technology, and that's so 11th century.
- use slightly curved basic strokes, not straight lines
- slight pressure sensitivity, slight rounded corners

