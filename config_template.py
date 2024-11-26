from collections import OrderedDict

clear_before_translate = OrderedDict({
   r'\n(Chapter.*?)\s*\[.*?Amazon.*?\].*?': r'\1',
   r'\n(.*?Amazon.*?)\n': '',
   r'\n(.*?author.*?)\n': '',
   r'\n(.*?Royal Road.*?)\n': '',
   r'\n(.*?Stole.*?;.*?)\n': '',
})