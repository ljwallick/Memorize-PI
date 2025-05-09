# Memorize-PI
A cool terminal tool that lets you memorize some PI, showing your mistakes and even allows compensation for skipping or adding digits, by default.

If you want to change how strict or lenient it is, go to the function `check_shifted_match()` and add a couple parameters in order or by kwarg
- `window`: The amount of digits it will check if you added/skipped some
- `match_level`: How many digits you want to be correct in a row to determine a(n) added/skipped group
- `extra_digs`: How many digits you want to add to the end to give a preview to help memorize more

That's it! You can use this tool to test and increase your PI memory. I currently have almost 60 digits memorized. More than the average person, for sure.
