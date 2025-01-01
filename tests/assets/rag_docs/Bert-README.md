# BERT

**\*\*\*\*\* New March 11th, 2020: Smaller BERT Models \*\*\*\*\***

This is a release of 24 smaller BERT models (English only, uncased, trained with WordPiece masking) referenced in [Well-Read Students Learn Better: On the Importance of Pre-training Compact Models](https://arxiv.org/abs/1908.08962).

We have shown that the standard BERT recipe (including model architecture and training objective) is effective on a wide range of model sizes, beyond BERT-Base and BERT-Large. The smaller BERT models are intended for environments with restricted computational resources. They can be fine-tuned in the same manner as the original BERT models. However, they are most effective in the context of knowledge distillation, where the fine-tuning labels are produced by a larger and more accurate teacher.

Our goal is to enable research in institutions with fewer computational resources and encourage the community to seek directions of innovation alternative to increasing model capacity.

You can download all 24 from [here][all], or individually from the table below:

|   |H=128|H=256|H=512|H=768|
|---|:---:|:---:|:---:|:---:|
| **L=2**  |[**2/128 (BERT-Tiny)**][2_128]|[2/256][2_256]|[2/512][2_512]|[2/768][2_768]|
| **L=4**  |[4/128][4_128]|[**4/256 (BERT-Mini)**][4_256]|[**4/512 (BERT-Small)**][4_512]|[4/768][4_768]|
| **L=6**  |[6/128][6_128]|[6/256][6_256]|[6/512][6_512]|[6/768][6_768]|
| **L=8**  |[8/128][8_128]|[8/256][8_256]|[**8/512 (BERT-Medium)**][8_512]|[8/768][8_768]|
| **L=10** |[10/128][10_128]|[10/256][10_256]|[10/512][10_512]|[10/768][10_768]|
| **L=12** |[12/128][12_128]|[12/256][12_256]|[12/512][12_512]|[**12/768 (BERT-Base)**][12_768]|

Note that the BERT-Base model in this release is included for completeness only; it was re-trained under the same regime as the original model.

Here are the corresponding GLUE scores on the test set:

|Model|Score|CoLA|SST-2|MRPC|STS-B|QQP|MNLI-m|MNLI-mm|QNLI(v2)|RTE|WNLI|AX|
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|BERT-Tiny|64.2|0.0|83.2|81.1/71.1|74.3/73.6|62.2/83.4|70.2|70.3|81.5|57.2|62.3|21.0|
|BERT-Mini|65.8|0.0|85.9|81.1/71.8|75.4/73.3|66.4/86.2|74.8|74.3|84.1|57.9|62.3|26.1|
|BERT-Small|71.2|27.8|89.7|83.4/76.2|78.8/77.0|68.1/87.0|77.6|77.0|86.4|61.8|62.3|28.6|
|BERT-Medium|73.5|38.0|89.6|86.6/81.6|80.4/78.4|69.6/87.9|80.0|79.1|87.7|62.2|62.3|30.5|

For each task, we selected the best fine-tuning hyperparameters from the lists below, and trained for 4 epochs:
- batch sizes: 8, 16, 32, 64, 128
- learning rates: 3e-4, 1e-4, 5e-5, 3e-5

If you use these models, please cite the following paper:

```
@article{turc2019,
  title={Well-Read Students Learn Better: On the Importance of Pre-training Compact Models},
  author={Turc, Iulia and Chang, Ming-Wei and Lee, Kenton and Toutanova, Kristina},
  journal={arXiv preprint arXiv:1908.08962v2 },
  year={2019}
}
```

[2_128]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-2_H-128_A-2.zip
[2_256]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-2_H-256_A-4.zip
[2_512]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-2_H-512_A-8.zip
[2_768]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-2_H-768_A-12.zip
[4_128]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-4_H-128_A-2.zip
[4_256]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-4_H-256_A-4.zip
[4_512]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-4_H-512_A-8.zip
[4_768]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-4_H-768_A-12.zip
[6_128]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-6_H-128_A-2.zip
[6_256]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-6_H-256_A-4.zip
[6_512]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-6_H-512_A-8.zip
[6_768]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-6_H-768_A-12.zip
[8_128]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-8_H-128_A-2.zip
[8_256]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-8_H-256_A-4.zip
[8_512]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-8_H-512_A-8.zip
[8_768]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-8_H-768_A-12.zip
[10_128]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-10_H-128_A-2.zip
[10_256]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-10_H-256_A-4.zip
[10_512]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-10_H-512_A-8.zip
[10_768]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-10_H-768_A-12.zip
[12_128]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-12_H-128_A-2.zip
[12_256]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-12_H-256_A-4.zip
[12_512]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-12_H-512_A-8.zip
[12_768]: https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-12_H-768_A-12.zip
[all]: https://storage.googleapis.com/bert_models/2020_02_20/all_bert_models.zip

**\*\*\*\*\* New May 31st, 2019: Whole Word Masking Models \*\*\*\*\***

This is a release of several new models which were the result of an improvement
the pre-processing code.

In the original pre-processing code, we randomly select WordPiece tokens to
mask. For example:

`Input Text: the man jumped up , put his basket on phil ##am ##mon ' s head`
`Original Masked Input: [MASK] man [MASK] up , put his [MASK] on phil
[MASK] ##mon ' s head`

The new technique is called Whole Word Masking. In this case, we always mask
*all* of the the tokens corresponding to a word at once. The overall masking
rate remains the same.

`Whole Word Masked Input: the man [MASK] up , put his basket on [MASK] [MASK]
[MASK] ' s head`

The training is identical -- we still predict each masked WordPiece token
independently. The improvement comes from the fact that the original prediction
task was too 'easy' for words that had been split into multiple WordPieces.

This can be enabled during data generation by passing the flag
`--do_whole_word_mask=True` to `create_pretraining_data.py`.

Pre-trained models with Whole Word Masking are linked below. The data and
training were otherwise identical, and the models have identical structure and
vocab to the original models. We only include BERT-Large models. When using
these models, please make it clear in the paper that you are using the Whole
Word Masking variant of BERT-Large.

*   **[`BERT-Large, Uncased (Whole Word Masking)`](https://storage.googleapis.com/bert_models/2019_05_30/wwm_uncased_L-24_H-1024_A-16.zip)**:
    24-layer, 1024-hidden, 16-heads, 340M parameters

*   **[`BERT-Large, Cased (Whole Word Masking)`](https://storage.googleapis.com/bert_models/2019_05_30/wwm_cased_L-24_H-1024_A-16.zip)**:
    24-layer, 1024-hidden, 16-heads, 340M parameters

Model                                    | SQUAD 1.1 F1/EM | Multi NLI Accuracy
---------------------------------------- | :-------------: | :----------------:
BERT-Large, Uncased (Original)           | 91.0/84.3       | 86.05
BERT-Large, Uncased (Whole Word Masking) | 92.8/86.7       | 87.07
BERT-Large, Cased (Original)             | 91.5/84.8       | 86.09
BERT-Large, Cased (Whole Word Masking)   | 92.9/86.7       | 86.46

**\*\*\*\*\* New February 7th, 2019: TfHub Module \*\*\*\*\***

BERT has been uploaded to [TensorFlow Hub](https://tfhub.dev). See
`run_classifier_with_tfhub.py` for an example of how to use the TF Hub module,
or run an example in the browser on
[Colab](https://colab.sandbox.google.com/github/google-research/bert/blob/master/predicting_movie_reviews_with_bert_on_tf_hub.ipynb).

**\*\*\*\*\* New November 23rd, 2018: Un-normalized multilingual model + Thai +
Mongolian \*\*\*\*\***

We uploaded a new multilingual model which does *not* perform any normalization
on the input (no lower casing, accent stripping, or Unicode normalization), and
additionally inclues Thai and Mongolian.

**It is recommended to use this version for developing multilingual models,
especially on languages with non-Latin alphabets.**

This does not require any code changes, and can be downloaded here:

*   **[`BERT-Base, Multilingual Cased`](https://storage.googleapis.com/bert_models/2018_11_23/multi_cased_L-12_H-768_A-12.zip)**:
    104 languages, 12-layer, 768-hidden, 12-heads, 110M parameters

**\*\*\*\*\* New November 15th, 2018: SOTA SQuAD 2.0 System \*\*\*\*\***

We released code changes to reproduce our 83% F1 SQuAD 2.0 system, which is
currently 1st place on the leaderboard by 3%. See the SQuAD 2.0 section of the
README for details.

**\*\*\*\*\* New November 5th, 2018: Third-party PyTorch and Chainer versions of
BERT available \*\*\*\*\***

NLP researchers from HuggingFace made a
[PyTorch version of BERT available](https://github.com/huggingface/pytorch-pretrained-BERT)
which is compatible with our pre-trained checkpoints and is able to reproduce
our results. Sosuke Kobayashi also made a
[Chainer version of BERT available](https://github.com/soskek/bert-chainer)
(Thanks!) We were not involved in the creation or maintenance of the PyTorch
implementation so please direct any questions towards the authors of that
repository.

**\*\*\*\*\* New November 3rd, 2018: Multilingual and Chinese models available
\*\*\*\*\***

We have made two new BERT models available:

*   **[`BERT-Base, Multilingual`](https://storage.googleapis.com/bert_models/2018_11_03/multilingual_L-12_H-768_A-12.zip)
    (Not recommended, use `Multilingual Cased` instead)**: 102 languages,
    12-layer, 768-hidden, 12-heads, 110M parameters
*   **[`BERT-Base, Chinese`](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)**:
    Chinese Simplified and Traditional, 12-layer, 768-hidden, 12-heads, 110M
    parameters

We use character-based tokenization for Chinese, and WordPiece tokenization for
all other languages. Both models should work out-of-the-box without any code
changes. We did update the implementation of `BasicTokenizer` in
`tokenization.py` to support Chinese character tokenization, so please update if
you forked it. However, we did not change the tokenization API.

For more, see the
[Multilingual README](https://github.com/google-research/bert/blob/master/multilingual.md).

**\*\*\*\*\* End new information \*\*\*\*\***

## Introduction

**BERT**, or **B**idirectional **E**ncoder **R**epresentations from
**T**ransformers, is a new method of pre-training language representations which
obtains state-of-the-art results on a wide array of Natural Language Processing
(NLP) tasks.

Our academic paper which describes BERT in detail and provides full results on a
number of tasks can be found here:
[https://arxiv.org/abs/1810.04805](https://arxiv.org/abs/1810.04805).

To give a few numbers, here are the results on the
[SQuAD v1.1](https://rajpurkar.github.io/SQuAD-explorer/) question answering
task:

SQuAD v1.1 Leaderboard (Oct 8th 2018) | Test EM  | Test F1
------------------------------------- | :------: | :------:
1st Place Ensemble - BERT             | **87.4** | **93.2**
2nd Place Ensemble - nlnet            | 86.0     | 91.7
1st Place Single Model - BERT         | **85.1** | **91.8**
2nd Place Single Model - nlnet        | 83.5     | 90.1

And several natural language inference tasks:

System                  | MultiNLI | Question NLI | SWAG
----------------------- | :------: | :----------: | :------:
BERT                    | **86.7** | **91.1**     | **86.3**
OpenAI GPT (Prev. SOTA) | 82.2     | 88.1         | 75.0

Plus many other tasks.

Moreover, these results were all obtained with almost no task-specific neural
network architecture design.

If you already know what BERT is and you just want to get started, you can
[download the pre-trained models](#pre-trained-models) and
[run a state-of-the-art fine-tuning](#fine-tuning-with-bert) in only a few
minutes.

## What is BERT?

BERT is a method of pre-training language representations, meaning that we train
a general-purpose "language understanding" model on a large text corpus (like
Wikipedia), and then use that model for downstream NLP tasks that we care about
(like question answering). BERT outperforms previous methods because it is the
first *unsupervised*, *deeply bidirectional* system for pre-training NLP.

*Unsupervised* means that BERT was trained using only a plain text corpus, which
is important because an enormous amount of plain text data is publicly available
on the web in many languages.

Pre-trained representations can also either be *context-free* or *contextual*,
and contextual representations can further be *unidirectional* or
*bidirectional*. Context-free models such as
[word2vec](https://www.tensorflow.org/tutorials/representation/word2vec) or
[GloVe](https://nlp.stanford.edu/projects/glove/) generate a single "word
embedding" representation for each word in the vocabulary, so `bank` would have
the same representation in `bank deposit` and `river bank`. Contextual models
instead generate a representation of each word that is based on the other words
in the sentence.

BERT was built upon recent work in pre-training contextual representations —
including [Semi-supervised Sequence Learning](https://arxiv.org/abs/1511.01432),
[Generative Pre-Training](https://blog.openai.com/language-unsupervised/),
[ELMo](https://allennlp.org/elmo), and
[ULMFit](http://nlp.fast.ai/classification/2018/05/15/introducting-ulmfit.html)
— but crucially these models are all *unidirectional* or *shallowly
bidirectional*. This means that each word is only contextualized using the words
to its left (or right). For example, in the sentence `I made a bank deposit` the
unidirectional representation of `bank` is only based on `I made a` but not
`deposit`. Some previous work does combine the representations from separate
left-context and right-context models, but only in a "shallow" manner. BERT
represents "bank" using both its left and right context — `I made a ... deposit`
— starting from the very bottom of a deep neural network, so it is *deeply
bidirectional*.

BERT uses a simple approach for this: We mask out 15% of the words in the input,
run the entire sequence through a deep bidirectional
[Transformer](https://arxiv.org/abs/1706.03762) encoder, and then predict only
the masked words. For example:

```
Input: the man went to the [MASK1] . he bought a [MASK2] of milk.
Labels: [MASK1] = store; [MASK2] = gallon
```

In order to learn relationships between sentences, we also train on a simple
task which can be generated from any monolingual corpus: Given two sentences `A`
and `B`, is `B` the actual next sentence that comes after `A`, or just a random
sentence from the corpus?

```
Sentence A: the man went to the store .
Sentence B: he bought a gallon of milk .
Label: IsNextSentence
```

```
Sentence A: the man went to the store .
Sentence B: penguins are flightless .
Label: NotNextSentence
```

We then train a large model (12-layer to 24-layer Transformer) on a large corpus
(Wikipedia + [BookCorpus](http://yknzhu.wixsite.com/mbweb)) for a long time (1M
update steps), and that's BERT.

Using BERT has two stages: *Pre-training* and *fine-tuning*.

**Pre-training** is fairly expensive (four days on 4 to 16 Cloud TPUs), but is a
one-time procedure for each language (current models are English-only, but
multilingual models will be released in the near future). We are releasing a
number of pre-trained models from the paper which were pre-trained at Google.
Most NLP researchers will never need to pre-train their own model from scratch.

**Fine-tuning** is inexpensive. All of the results in the paper can be
replicated in at most 1 hour on a single Cloud TPU, or a few hours on a GPU,
starting from the exact same pre-trained model. SQuAD, for example, can be
trained in around 30 minutes on a single Cloud TPU to achieve a Dev F1 score of
91.0%, which is the single system state-of-the-art.

The other important aspect of BERT is that it can be adapted to many types of
NLP tasks very easily. In the paper, we demonstrate state-of-the-art results on
sentence-level (e.g., SST-2), sentence-pair-level (e.g., MultiNLI), word-level
(e.g., NER), and span-level (e.g., SQuAD) tasks with almost no task-specific
modifications.
