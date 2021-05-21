# search-ranker
A small project for IR

## How to run?
First, go into folder `SEARCH-RANKER`:
```
cd search-ranker
```
Then use `python` command to run:
```
python main.py
```

## Instruction:
1. `xrawler.py`: scratch website of www.foxnews.com and get 200+ html files as a local dataset.
2. `iat_ws_python3.py`: API for transfer .mp3 file to the content of speech.
3. `src`: a folder containing the implement of the search-ranker algorithm. 

## Feature:
1. Inverted Index:
```
"word":{
    "doc_id":[pos_list]
}
```
2. Link Info:
```
"doc_id":{
    "topic":"great-outdoors"
    "headline":"Australian fisherman shows off giant rock lobster in TikTok video"
    "datePublished":"2021-05-13T04:00:23-04:00"
    "url":
}
```
3. Ranking algorithm:
   - VSM
   - wf-idf
   - to be continue
4. Query:
   - Single word
   - Multiple words 
   - Phrase (unfinished)
   - to be continue

5. Bonus feature:
    speech $\rightarrow$ text for query searching
