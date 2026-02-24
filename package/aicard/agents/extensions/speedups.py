def text_compression(text: str) -> str:
    #print("preprocessing text size "+str(len(text)))
    for symbol in "()[]*_/\\\"'`:;-+.,?\n\t\r=|><{}&!#$": # remove common symbols
        text = text.replace(symbol, " ")
    text = text.lower()
    found = dict()
    result = ""
    pos = 0
    window = float('inf') # after every set number of words allow repetition (large number to disable)
    for t in text.split(" "):
        pos += 1
        # convert to a set while preserving order to keep phrases
        if not t: continue
        prev_pos = found.get(t, None)
        found[t] = pos # do this here to preserve continuity of concepts
        if prev_pos and prev_pos>pos-window: continue
        result += " "+t
    result = "Respond with full sentences. Do not mention missing information. Here are keywords describing the model: "+result
    #print("reduced to size "+str(len(result)))
    return result