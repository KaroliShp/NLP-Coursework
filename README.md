# NLP-based Dialog System

Simple question answering system that is pre-trained on a user input. Coursework for Inf2A - Processing Formal and Natural Languages

## Example dialog

The following is an example dialog:

```
$$ John is a duck.
  OK

$$ John is orange.
  OK
  
$$ Mary is a frog.
  OK
 
$$ John likes Mary.
  OK

&& Who does John like?
  Mary

&& Who likes Mary?
  John

&& Which orange duck likes a frog?
  John
  
&& Who likes John?
  No one :'(

```

You can try it out by downloading ```semantics.py``` (make sure you have ```nltk``` installed) and running:

```
$ python semantics.py
```

It was developed using ```Python 2.7.5```, so will not work for newer versions (like ```3.x```)

## Implementation

Two main ideas were used in the coursework: CTF grammars and lambda calculus.

The solution uses CTF (context-free grammar) for processing statements and questions, for example:

```
Sentence -> P (Proper Noun) BEs (is, are) AR (article) N (Noun)
```

Syntactic parse trees are generated for each sentence, which are then given mathematical meaning using lambda calculus (for example ```Who is a duck?``` would translate to ```λx.Is_Duck(x)```). Lambda expressions can then be executed according to the fact base that is gathered from user input.
