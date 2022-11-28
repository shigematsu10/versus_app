from sumeval.metrics.rouge import RougeCalculator
 
 
rouge = RougeCalculator(stopwords=True, lang="en")
 
summary="This week, a U.S consumer advisory group set up by the Department of Transportation said at a public hearing that while the government is happy to set standards for animals flying on planes, it doesn't stipulate a minimum amount of space for humans. 'In a world where animals have more rights to space and food than humans,' said Charlie Leocha, consumer representative on the committee. They say that the shrinking space on aeroplanes is not only uncomfortable - it's putting our health and safety in danger."
references="Experts question if  packed out planes are putting passengers at risk . U.S consumer advisory group says minimum space must be stipulated . Safety tests conducted on planes with more leg room than airlines offer ."
 
rouge_1 = rouge.rouge_n(
            summary=summary,
            references=references,
            n=1)
 
rouge_2 = rouge.rouge_n(
            summary=summary,
            references=references,
            n=2)
 
rouge_l = rouge.rouge_l(
            summary=summary,
            references=references)
 
rouge_be = rouge.rouge_be(
            summary=summary,
            references=references)
 
print("ROUGE-1: {}, ROUGE-2: {}, ROUGE-L: {}, ROUGE-BE: {}".format(
    rouge_1, rouge_2, rouge_l, rouge_be
).replace(", ", "\n"))