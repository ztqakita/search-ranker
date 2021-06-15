import os
import util
import json
import re
import speech
from SpellingCorrect import spell
from InvertedIndex import constructIndex, getIndex
from AnalyzeRank import analyzeInput, calculateRank
from PreprocessText import stemming
from search_ranker_pictures import output_fig_in_1_window

FILE_NUM = len(os.listdir(util.docs_path))

if __name__ == "__main__":
    # constructIndex.construct_index(util.docs_path)
    inverted_index = getIndex.get_index()
    word_list = getIndex.get_word_list()
    VSM = calculateRank.createVSM(inverted_index, word_list, FILE_NUM, util.docs_path)
    loop = True

    while loop:
        print("searching operation: ")
        print("[1] VSM [2] Voice Input [3] Image Retrieval [4] Exit")
        print("your choice(int):")
        try:
            choice = int(input())
            if choice == 7:
                break
        except:
            print()
            continue

        if choice >= 1 and choice <= 6:
            # print("input the query statement:")
            # STATEMENT = input()
            # if STATEMENT == "EXIT":
            #     break

            # 查询排序
            if choice == 1:
                print("input the query statement:")
                raw_query = input()
                print("stemming...")
                query = stemming.lemmatize_sentence(raw_query, True)
                print(str(query))
                print("spelling correcting...")
                query = spell.correctSentence(query)
                print(str(query))

                word_set = set(query)

                word_vector = calculateRank.create_query_vector(word_list, word_set)
                print("VSM method:")
                sorted_doc_list = calculateRank.calculate_cos(VSM, word_vector)
                vsm_doc_list = []
                for doc in sorted_doc_list:
                    vsm_doc_list.append(int(doc[1]))
                    with open(util.project_path + 'linkInfo.json', 'r') as f:
                        _str = f.read()
                        link_info = json.JSONDecoder().decode(_str)
                        info = link_info[doc[1]]
                        print("doc id:", doc[1], "score:", "%.4f" % doc[0])
                        print("topic: ", info["topic"], "headline: ", info["headline"], "datePublished: ", info["datePublished"]
                              , "url: ", info["url"])
                        f = open(util.docs_path + '\\' + doc[1] + '.html', encoding='utf-8')
                        text = f.read()
                        for word in query:
                            # loc = inverted_index[word][doc[1]][0]
                            # loc_raw = re.match(word, text)
                            loc = text.find(word)
                            if loc != -1:
                                print("match content: ", "...", text[max(0, loc - 50):loc + 50] + "...\n")
                            else:
                                if doc[1] in inverted_index[word].keys():
                                    loc = inverted_index[word][doc[1]][0]
                                    print("match content: ", "the", loc, "th place of text\n")
                            # if loc_raw is not None:
                            #     _loc = loc_raw.span()
                            #     loc = _loc[0]
                            #     print(word, loc)
                            #     break
                        # print("match content: ", "...", text[max(0, loc - 50):loc + 50] + "...\n")

                doc_list = analyzeInput.analyze_union_input(inverted_index, word_set)
                sorted_doc_list_2 = calculateRank.get_sorted_score_list(inverted_index, FILE_NUM, doc_list, word_set)
                print("wf-idf union method:")
                wfidf_doc_list = []
                for doc in sorted_doc_list_2:
                    wfidf_doc_list.append(int(doc[1]))

                    # print("doc id:", doc[1], "score:", "%.4f" % doc[0])

                print("VSM result: ", len(vsm_doc_list))
                print("Union: ", len(wfidf_doc_list))
                accuracy = len(wfidf_doc_list) / len(vsm_doc_list)
                print("accuracy:", accuracy)

                doc_list = analyzeInput.analyze_inter_input(inverted_index, word_set)
                sorted_doc_list_2 = calculateRank.get_sorted_score_list(inverted_index, FILE_NUM, doc_list, word_set)
                print("wf-idf intersection method:")
                wfidf_doc_list = []
                for doc in sorted_doc_list_2:
                    wfidf_doc_list.append(int(doc[1]))

                    # print("doc id:", doc[1], "score:", "%.4f" % doc[0])

                sum = 0
                diff = 0
                print("VSM result: ", len(vsm_doc_list))
                print("Intersection: ", len(wfidf_doc_list))
                accuracy = len(wfidf_doc_list) / len(vsm_doc_list)
                print("accuracy:", accuracy)

            elif choice == 2:
                voice_path = util.docs_path.replace("docs", "speech")
                real_path = voice_path + "\\t3.mp3"
                speech.sound2text(real_path)
                text = ''
                with open('./speech_result.txt', 'r', encoding='UTF-8') as fp:
                    text = fp.read()
                os.remove('./speech_result.txt')
                os.remove('./trial.pcm')
                print("stemming...")
                query = stemming.lemmatize_sentence(text, True)
                print(str(query))
                print("spelling correcting...")
                query = spell.correctSentence(query)
                print(str(query))

                word_set = set(query)

                word_vector = calculateRank.create_query_vector(word_list, word_set)
                print("VSM method:")
                sorted_doc_list = calculateRank.calculate_cos(VSM, word_vector)
                vsm_doc_list = []
                for doc in sorted_doc_list:
                    vsm_doc_list.append(int(doc[1]))
                    with open(util.project_path + 'linkInfo.json', 'r') as f:
                        _str = f.read()
                        link_info = json.JSONDecoder().decode(_str)
                        info = link_info[doc[1]]
                        print("doc id:", doc[1], "score:", "%.4f" % doc[0])
                        print("topic: ", info["topic"], "headline: ", info["headline"], "datePublished: ", info["datePublished"]
                              , "url: ", info["url"])
                        f = open(util.docs_path + '\\' + doc[1] + '.html', encoding='utf-8')
                        text = f.read()
                        for word in query:
                            # loc = inverted_index[word][doc[1]][0]
                            # loc_raw = re.match(word, text)
                            loc = text.find(word)
                            if loc != -1 and word != "be":
                                print("match content: ", "...", text[max(0, loc - 50):loc + 50] + "...\n")
                            else:
                                if doc[1] in inverted_index[word].keys():
                                    loc = inverted_index[word][doc[1]][0]
                                    # print("match content: ", "the", loc, "th place of text\n")
                            # if loc_raw is not None:
                            #     _loc = loc_raw.span()
                            #     loc = _loc[0]
                            #     print(word, loc)
                            #     break
                        # print("match content: ", "...", text[max(0, loc - 50):loc + 50] + "...\n")

                doc_list = analyzeInput.analyze_union_input(inverted_index, word_set)
                sorted_doc_list_2 = calculateRank.get_sorted_score_list(inverted_index, FILE_NUM, doc_list, word_set)
                print("wf-idf union method:")
                wfidf_doc_list = []
                for doc in sorted_doc_list_2:
                    wfidf_doc_list.append(int(doc[1]))

                    # print("doc id:", doc[1], "score:", "%.4f" % doc[0])

                print("VSM result: ", len(vsm_doc_list))
                print("Union: ", len(wfidf_doc_list))
                accuracy = len(wfidf_doc_list) / len(vsm_doc_list)
                print("accuracy:", accuracy)

                doc_list = analyzeInput.analyze_inter_input(inverted_index, word_set)
                sorted_doc_list_2 = calculateRank.get_sorted_score_list(inverted_index, FILE_NUM, doc_list, word_set)
                print("wf-idf intersection method:")
                wfidf_doc_list = []
                for doc in sorted_doc_list_2:
                    wfidf_doc_list.append(int(doc[1]))

                    # print("doc id:", doc[1], "score:", "%.4f" % doc[0])

                sum = 0
                diff = 0
                print("VSM result: ", len(vsm_doc_list))
                print("Intersection: ", len(wfidf_doc_list))
                accuracy = len(wfidf_doc_list) / len(vsm_doc_list)
                print("accuracy:", accuracy)

            elif choice == 3:
                image_index = getIndex.get_Image_Index()
                print("input the query statement:")
                raw_query = input()
                route = util.project_path + "src\\search_ranker_pictures\\cifar_100_selected\\"
                flag = 0
                if str(raw_query) in list(image_index.keys()):
                    flag = 1
                    output_fig_in_1_window.output_in_all_dirs(route + raw_query)
                else:
                    for key in image_index.keys():
                        if str(raw_query) in image_index[key].keys():
                            flag = 1
                            output_fig_in_1_window.output_in_one_dir(route + key + "\\" + raw_query)

                if flag == 0:
                    print("I am sorry! The input query doesn't exist in our image dataset!")
            elif choice == 4:
                print("Byebye!")
                break
            else:
                print("Invalid choice! Please observe these choices carefully!")