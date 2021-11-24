# CISC/CMPE 422: Formal Methods in Software Engineering (Fall 2021)
## Assignment 3: Object Modelling With Alloy
## Due date: Mon, Nov 8, 5pm EST (GitHub classroom and OnQ submission)

## Software
This assignment uses Alloy, an analysis tool for object models developed by the [Software Design Group](https://sdg.csail.mit.edu/) at MIT. Alloy is publicly available for Solaris, Windows, Linux and Mac OS/X. So, if you have access to a PC running Windows or Linux, or to a Mac running OS/X, you can [download](https://alloytools.org/download.html) and install it. Installation is straightforward. Otherwise, Alloy also is installed in CasLab. Just type `java -jar <name>.jar` on the command line where `<name>` is the name of the Alloy jar file. 

## Learning Outcomes
The purpose of this assignment is to give you
- practical experience with
  - expressing objects and their relationships formally using constraints expressed in first-order logic and a relational calculus, and
  - reasoning about objects, their relationships and operations on them using constraint solving, and
- an increased understanding of file dependencies and makefiles.

## Questions
### Part I: Files and timestamps (22/104 points)

#### File to Edit

Please enter your Alloy specifications for this part into the given file [a3Part1.als](a3Part1.als).

#### Preparation (0 points)

Consider the following Alloy object model:

```Alloy
module A3Part1

open util/ordering[Time]

sig Time {}      // instances denote timestamps

sig File {
    time : Time  // every file has exactly one timestamp
}
```

We will call elements of signature `File` 'files' and elements of signature `Time` 'timestamps'. Use Alloy's `run` command as in, e.g., 

```Alloy
runPrep1: run {} for 3 
runPrep2: run {some File} for 3
runPrep3: run {some f1, f2 : File | f1 != f2 && f1.time = f2.time} for 3
```

to create Alloy instances satisfying all constraints expressed in the model and the additional constraints that are provided as arguments to the command. 

See [models/util/ordering.als](doc/ordering.als) (from Alloy's .jar file, but included in the directory `doc/` of this assignment's repository for convenient reference), for descriptions of some of the functions (e.g., `first`, `last`, `next`, and `max`) and predicates (`lt`, `lte`, `gt`, and `gte`) that the `ordering` module comes with. Given an instance, use the evaluator to experiment with these functions and predicates. Due to the constraints that the `ordering` module imposes, timestamps will form a total linear order, starting with `Time0`, `Time1`, `Time2`, ... (or, `Time$0`, `Time$1`, ... in the evaluator). We will assume that the lowest (smallest) element in this ordering (`Time0`) represents the oldest timestamp. That is, we will consider timestamps lower in this ordering as older, and timestamps higher (greater) in this ordering as more recent (younger). Concretely, given two time stamps `t1` and `t2`, we will call `t1` 'more recent than' `t2` (or `t2` 'older than' `t1`) if and only if `gt[t1,t2]` (or `lt[t2,t1]`) holds. Consequently, given an Alloy instance, function `first` (from module `ordering`) denotes the lowest timestamp in the ordering in the instance (in this assignment typically represented by `Time0`) and thus the oldest timestamp. In contrast, function `last` denotes the highest and thus most recent (youngest) timestamp. Given two files `f1` and `f2`, we will call `f1` 'older than' `f2` if and only if the timestamp of `f1` is older than that of `f2`, i.e., `lt[f1.time, f2.time]`. Similarly, we will call `f1` 'more recent' than `f2` if and only if the timestamp of `f1` is more recent than that of `f2`, i.e., `gt[f1.time,f2.time]`.

#### Question 1: Basic, time-related functions (12 points)

- Express each of the following four functions formally in Alloy and add them to the model above.
  - (**3 points**) Question 1a: *Function `getOldest[] : set File` returns the set of oldest files (if any).*
  - (**3 points**) Question 1b: *Function `getMostRecent[] : set File` returns the set of most recent files (if any).*
  - (**3 points**) Question 1c: *Function `getSecondOldest[] : set File` returns the set of second-oldest files (if any), i.e., all files whose timestamp `t2` is such that `t2` is more recent than the timestamp `t1` of the oldest files and there are no files with a timestamp `t` that 'lies between `t1` and `t2`' (i.e., `t1` is less than `t`, and `t` is less than `t2`).*
  - (**3 points**) Question 1d: *Given a set `F` of files, function `getTime[F : set File] : Time` returns the most recent timestamp of any of the files in `F`.* 

- Use the `run` command to create instances and test your definition of these functions, as in, e.g.:
```Alloy
runQ1a: run {some getOldest[] && some getMostRecent[]} for 3
```

#### Question 2: Basic, time-related properties (10 points)

- For each of the two statements below, create an assertion (named `Q2a` and `Q2b`, respectively) that captures its meaning. Hint: Use `getTime[F : set File] : Time`.
  - (**3 points**) Q2a: *The second-oldest files are always more recent than the oldest files.*
  - (**3 points**) Q2b: *The second-oldest files are always older than the most recent files.*
- (**4 points**) Use the Alloy analyzer to see if assertions `Q2a` and `Q2b` hold. Start with a small scope (such as 1 or 2) and, if there are no counter examples, work your way up to at least scope 6. For each assertion, add a comment to the definition of the assertion in the Alloy file indicating whether or not it holds. If it fails in some scope, use Alloy to create a counter example in the smallest possible scope and submit it as part of your answers for this part. Hint: one assertion should hold, while the other should fail! 

### Part II: States and expressing change (21 points)

#### File to Edit

Please enter your Alloy specifications for this part into the given file [a3Part2.als](a3Part2.als).

#### Preparation (0 points)

The object model in the previous part does not allow us to express changes to the timestamps of files. This, however, is certainly something that the execution of a makefile does. So, in preparation for Part III below, we add the notion of `State`. Consider:

```Alloy
module A3Part2

open util/ordering[Time]

sig Time {}

sig File {}
  
sig State {
   time: File set -> one Time  // every file has exactly one time stamp 
}

runPrep1: run {some State} for 3
```

Note that different states (i.e., instances of signature `State`) can assign different timestamps to files (i.e., for two states `s1` and `s2`, the binary relations `s1.time` and `s2.time` may be completely different), allowing us to express how an operation might change the age of files. Use the `run` command to generate a few instances, and make sure you understand them.

#### Question 3: Basic, time-related changes (6 points)

Formalize each of the following two predicates in Alloy and add them to the model shown at the beginning of Part II.
- (**3 points**) Question 3a: *Predicate `setToSmallerTimestamp[s, s' : State]` holds precisely if, going from `s` to `s'`, the timestamp of every file gets smaller. I.e., the timestamp of a file `f` in `s'` is less than the timestamp of `f` in `s`.*
- (**3 points**) Question 3b: *Predicate `setToNextTimestamp[s, s': State]` holds precisely iff the timestamp of a file `f` in `s'` is exactly one step greater than the timestamp of `f` in `s`.*

Use Alloy's `run` command as illustrated below to create Alloy instances and test your definitions of these predicates.

```Alloy
runQ31: run {some s, s': State | setToSmallerTimestamp[s, s']} for 3 but exactly 2 State
```

#### Question 4: Properties of basic, time-related changes (15 points)

We can view the predicates `setToSmallerTimestamp[s, s']` and `setToNextTimestamp[s, s']` as declaratively specified operations that, whenever they hold, transform the state `s` into a state `s'`. The formulas making up the body of the definition of these functions define the relationship between `s` and `s'`. We now want to analyze these two operations with respect to some properties.

- (**3 points**) Question 4a: Create a function `getMostRecent[s : State] : set File` that returns the set of files that are the most recent in state `s` (i.e., they have the most recent timestamp of all files).
- (**8 points**) Question 4b: Do `setToSmallerTimestamp[s,s']` and `setToNextTimestamp[s,s']` preserve the set of most recent files, i.e., assuming that, e.g., `setToSmallerTimestamp[s,s']` holds, do `s` and `s'` have the same set of most recent files? Formulate two assertions, named `Q4b1` and `Q4b2` respectively, that allow you to check this. As before, to check these assertions, use the Alloy analyzer with increasingly larger scopes until scope 6 and indicate the result as a comment to the assertion itself. Hint: one assertion holds, while the other does not.
- (**4 points**) Question 4c: What if state `s` contains a file `f` that has the most recent possible (in the Alloy instance generated) timestamp (denoted by function `last`)? Does this have any impact on the operations above, i.e., does it impact Alloy's ability to find a state `s'` such that `setToSmallerTimestamp[s,s']` and `setToNextTimestamp[s,s']` hold? Add the following to your Alloy model and check both assertions (up to scope 6).

    ```Alloy
    pred noTimeLeft[s : State] {
        some (s.time).last
        // or, equivalently, max[File.(s.time)] = last
    }
    
    // "if there's no time left in s, setToSmallerTimestamp[s,s'] fails"
    assert ifNoTimeLeftSetToSmallerTimestampFails {
        all s : State | noTimeLeft[s] => all s' : State | !setToSmallerTimestamp[s, s']
    }
    
    // "if there's no time left in s, setToNextTimestamp[s,s'] fails"
    assert ifNoTimeLeftSetToNextTimestampFails {
        all s : State | noTimeLeft[s] => all s' : State | !setToNextTimeStamp[s, s']
    }
    ```

    Make sure you understand the results of the analysis. For each of the two assertions record, as a comment next to the assertion, whether it holds or not. Also, in case an assertion fails, use Alloy to create a counter example in the smallest possible scope and submit it as part of your answers for this part. Hint: one assertion should hold and other should fail.

### Part III: Formalizing and analyzing 'make' (61 points)

#### File to Edit

Please enter your Alloy specifications for this part into the given file [a3Part3.als](a3Part3.als).

#### Preparation (0 points)

*Background on makefiles*: A makefile consists of rules, each of which having exactly one 'target' file and a collection of 'prerequisite' files. A rule typically also has commands that are executed when the rule is executed and that lead to the 'making' (i.e., (re-)building) of the target. The invocation of `make t` where `t` is a target with makefile `mf`, causes the following recursive process: in `mf`, look up the rule `r` associated with `t`; if a prerequisite in that rule is itself a target, it is made, if necessary; then, if a prerequisite has a timestamp more recent than `t`, then `t` is made by executing the commands in `r`. The invocation of `make all` invokes `make` on all targets in the makefile. Building systems using 'make' was covered in CISC 220, but there also is a lot of information available online, including, e.g., [ftp://ftp.gnu.org/old-gnu/Manuals/make-3.79.1/html_chapter/make_2.html](ftp://ftp.gnu.org/old-gnu/Manuals/make-3.79.1/html_chapter/make_2.html).

The following Alloy model will allow us to formalize and reason about some key aspects of the 'make' process. The model contains many of the core concepts of make (e.g., files with timestamps and dependencies, and rules with targets and prerequisites), while ignoring others (e.g., commands, file contents). 

```Alloy
module A3Part3

open util/ordering[Time]

sig File {}

sig Time {}

sig State {
    time : File set -> one Time,
    dependsOn : File set -> set File
}
fact StateFacts {
    // 'dependsOn' is acyclic
    all s : State | no f : File | f->f in ^(s.dependsOn)     
    // or, equivalently: all s : State | no f : File | f in f.^(s.dependsOn) 
}

sig Rule {
    target : File,
    prereqs : set File
}
fact RuleFacts {
    all r1, r2 : Rule | r1 != r2 => r1.target != r2.target     // different rules have different targets
    all r : Rule | some r.prereqs     // no rules without prerequisites
}

sig Makefile { 
    rules : set Rule,
    targets : set File,
    hasAsPrereq : File set -> set File
}
fact MakefileFacts {
    // the targets of a makefile are all files that have prerequisites 
    all mf : Makefile | mf.targets = (mf.hasAsPrereq).File
    // no extra rules, i.e., every rule belongs to a makefile
    all r : Rule | some mf : Makefile | r in mf.rules
    // define dependencies among file according to rules
    all mf : Makefile | mf.hasAsPrereq = {f:File, f':File | some r : Rule | f = r.target && f' in r.prereqs}
    // no circular dependencies in rules
    all mf : Makefile | no f : File | f->f in ^(mf.hasAsPrereq)
}
```

Concretely, the model uses signatures `Time`, `File`, and `State`, as before, except that a state now also has binary-relation-valued attribute `dependsOn` that records which files a given file depends on in that state (due to, e.g., 'include' statements). `StateFacts` ensures that this dependency relation does not contain any cycles. As mentioned, our formalization will ignore commands. In our formalization, a makefile also has an attribute `targets` and a binary-relation-valued attribute `hasAsPrereq` that records which target has which prerequisites. `RuleFacts` ensures that two rules do not have the same target and that the set of prerequisites of a rule is not empty. `MakefileFacts` ensures that the `target` and `hasAsPrereq` attribute carry the correct value, that every rule belongs to a makefile, and that `hasAsPrereq` does not contain any cycles. 

Consider, for instance, the content of the makefile `makefile0`, shown just below this paragraph. An Alloy instance satisfying all the constraints above, and showing the rules (named `rule0` and `rule1`) in the makefile, is shown in a picture just below `makefile0`.

```Alloy
file3: file1
file2: file0 file3
```

![makefileInstance3](doc/makefileInstance3.png)

Note that the values of the attributes `hasAsPrereq` and `targets` are shown inside the box for `makefile0` and not as arrows.

The 'current time' of a state `s` is the largest timestamp used by a file in `s`. Function `getTime[s : State] : Time` returns the current time of its argument state. We call the timestamp that follows `getTime[s]` in the ordering (i.e., `getTime[s].next`) the 'next available time' in `s`. Note that a state may not have a next available time. A file `f` is considered 'fresh (i.e., not stale) in some state `s` according to some makefile `mf`' if and only if `f` is not older than any of its prerequisites. Predicate `freshAccordingToMakefile[f, mf, s]` captures this. The effect of executing makefile `mf` in state `s` is captured by predicate `make[mf, s, s']` which holds for a state `s'` if and only if, in `s'`,
- the `dependsOn` relation is unchanged, and
- the timestamps of (a) all targets that are stale according to `mf` and of (b) all files that have a stale target as a transitive prerequisite are equal to the next available time, and
- the timestamps of all other files are unchanged,

where a target `f1` is said to have a file `fn` as 'transitive prerequisite' if there is a sequence of files `f1`, `f2`, ..., `fn` such that `n` is greater than `1` and `fi+1` is a prerequisite of target `fi` for all `1 ≤ i < n`. 

#### Question 5: Formalization and first analysis of 'make' (3 points)

The definition of the `make` predicate found in the initial file [a3Part3.als](a3Part3.als) is incomplete. Complete the formalization of make. Use Alloy's run command as illustrated below to create Alloy instances and test your formalization of make.

```Alloy
runQ51: run {some mf:MakeFile, f:File, s:State, s':State-s | !freshAccordingToMakefile[f,mf,s'] && make[mf, s, s']} but exactly 1 Makefile, exactly 2 State
runQ52: run {some mf:MakeFile, s:State, s':State-s | make[mf, s, s']} but exactly 1 Makefile, exactly 2 State
```

#### Question 6: First analysis of 'make' (8 points)

Next, we want to express and check some initial properties of the make predicate.

- For each of the two statements below, create an assertion (named `Q6a` and `Q6b`, respectively) that captures its meaning:
  - (**3 points**) Q6a: *The result of `make` is uniquely defined, that is, if `make` holds for some start state `s`, some makefile `mf`, some resulting state `s'`, and also for `s`, `mf`, and some other resulting state `s''`, then the two result states `s'` and `s''` have the same `time` and `dependsOn` relations.*
  - (**3 points**) Q6b: *If the start state has no time left (in the sense of Question 4c), then `make` always fails.*
- (**2 points**) Use the Alloy Analyzer to determine which of these properties hold (using scope 6). For each property record, as a comment, whether it holds or not. Hint: one assertion should hold, while the other should fail. 

#### Question 7: Correctness of 'make' (9 points)

We will now explore the question of what it means for a makefile to be correct.

- (**3 points**) Add a predicate `fresh[f : File, s : State]` to your model that holds precisely if `f` is fresh in `s`, i.e., `f` is at least as recent as all of the files it depends on.
- (**3 points**) Add a predicate `fresh[s : State]` to your model that holds precisely if `s` is fresh, i.e., all files are fresh in `s`.
- (0 points) Use Alloy's `run` command to create Alloy instances and test your definitions of these predicates.
- (**3 points**) Create an assertion (named `Q7a`) that captures the meaning of the following statement:
  - Q7a: *`make` always creates a fresh state.* 
- (0 points) Use the Alloy analyzer to see if assertion `Q7a` holds (using scope 6). Hint: this assertion should fail. 

#### Question 8: Soundness of makefiles (15 points)

The reason `make` does not ensure freshness is that currently no relationship between the rules in the makefile and the dependencies among files is enforced.

- (**3 points**) Add a predicate `sound[mf : Makefile, s : State]` to your model that holds precisely when `mf` is sound with respect to `s`, i.e., whenever some file `f` depends on some file `f'` in `s`, then that relationship is reflected in a rule in `mf` that has `f` as target and `f'` as prerequisite.
- (0 points) Use Alloy's `run` command to create Alloy instances and test your definition.
- For each of the two statements below, create an assertion (named `Q8a` through `Q8d`, respectively) that captures its meaning:
  - (**3 points**) Q8a: *Soundness is preserved by the removal of dependencies, i.e., if a makefile is sound with respect to some state `s` and a state `s'` does not contain more file dependencies than `s`, then the makefile is also sound with respect to `s'`.*
  - (**3 points**) Q8b: *Soundness is preserved by the addition of rules and prerequisites, i.e., if a makefile `mf` is sound with respect to some state and a makefile `mf'` records the same prerequisite relationships as `mf` and possibly some additional ones, then `mf'` is also sound with respect to that same state.*
  - (**3 points**) Q8c: *If file `f` is stale in state `s`, a sound make in `s` results in a state `s'` in which the timestamps of all files depending on `f` are equal to the next available time in `s`.*
  - (**3 points**) Q8d: *Whenever `make` is used with a makefile that is sound with respect to the initial state, then it ensures a fresh resulting state.*
- (0 points) Use the Alloy Analyzer to determine which of these assertions hold (in scopes less than or equal to 6). For each assertion record whether it is implied or not. Hint: all four assertions should hold. 

#### Question 9: Optimality of makefiles (11 points)

Soundness ensures that a makefile creates a fresh state. However, to achieve this, the makefile might 'do more than necessary'.

- (**3 points**) Create a predicate `optimal[mf : Makefile, s : State]` that holds precisely when `mf` is optimal with respect to `s`, i.e., when `mf` is sound with respect to `s` and any prerequisite relationship in `mf` corresponds to a file dependency in `s`.
- (0 points) Use Alloy's `run` command to create Alloy instances and test your definition.
- For each of the following statements, formalize it as an assertion (named `Q9a` and `Q9b`, respectively):
  - (**3 points**) Q9a: *A make in a fresh state `s` using a makefile that is sound with respect to `s` does not change the timestamp of any file.*
  - (**3 points**) Q9b: *A make in a fresh state `s` using a makefile that is optimal with respect to `s` does not change the timestamp of any file.*
- (**2 points**) Use the analyzer to determine which of these statements hold (in scopes up to 6), and record the result in a comment. Hint: One assertion should fail, while the other should succeed. 

#### Question 10: Formalization and analysis of 'touch' operation (15 points)

- (**3 points**) Add a predicate `touch[f : File, s : State, s' : State]` to your model that holds precisely when `s` has time left, `s` and `s'` have the same file dependencies, the timestamp of `f` in `s'` is the next available timestamp in `s`, and the timestamps of all other files in `s'` are unchanged.
- Use Alloy's `run` command to create Alloy instances and test your definition.
- For each of the following statements, formalize it as an assertion (named `Q10a` through `Q10c`):
  - (**3 points**) Q10a: *Touching `f` sets the timestamp of `f` to the next available time in `s` and leaves the timestamps of all other files unchanged.*
  - (**3 points**) Q10b: *Touching a file results in a stale state.*
  - (**3 points**) Q10c: *An optimal make after `f` has been touched advances the time of `f'` if and only if `f'` depends transitively on `f`, i.e., if file `f` is touched in a fresh state, and an optimal make is performed on the resulting state, then make creates a state `s''` in which the timestamp of a different file `f'` is equal to the current time in `s''` if and only if `f'` depends transitively on `f`.*
- (**3 points**) Use the analyzer to determine which of these statements hold (in scopes up to 6), and record the result in a comment. 

### Part IV: Discussion (0 points)

- *Creating makefiles automatically*: As seen, for makefiles to work correctly they must reflect the dependencies between files (e.g., which file imports which other files). Fortunately, there are tools such as [CMake](https://cmake.org/) that inspect the files and automatically create a makefile that is guaranteed to reflect these dependencies, i.e., that, in terms of this assignment, is sound.
- *Abstraction at work*: As mentioned, our formalization of makefile ignores commands. Here are some other aspects of makefiles that we have ignored: file contents, exact time values, and the application order of rules. 

## Instructions
**Important: Please follow the instructions below carefully. Points may be taken off, if you don't.**

- Only edit the files [a3Part1.als](a3Part1.als), [a3Part2.als](a3Part2.als), and [a3Part3.als](a3Part3.als).
- In the following instructions, any files that you create (such as screen shots of counter examples) should be placed at the top level of the repository, i.e., in the same location as the three `.als` files that you edit.

### Part I
- Put your answers into the given file `a3Part1.als` (see beginning of Part I). Please ensure that it is clear which (sub-)question each answer corresponds to.
- Also, save screen shots of any counter examples found in Question 2 in files named `Q2CounterExample_x.ext` where `x` is either `a` (if the counter example demonstrates the failure of the assertion from Question 2a), or `b` (if the counter example demonstrates the failure of the assertion from Question 2b) and `ext` is the image file type. One counter example per failing assertion is enough. 

### Part II
- Put your answers into the given file `a3Part2.als` (see beginning of Part II). Please ensure that it is clear which (sub-)question each answer corresponds to.
- Also, save screen shots of any counter examples found in Question 4 in files named `Q4CounterExample_x.ext` where `x` is either `setToSmaller` (if the counter example demonstrates the failure of assertion `ifNoTimeLeftSetToSmallerTimestampFails`) or `setToNext` (if the counter example demonstrates the failure of assertion `ifNoTimeLeftSetToNextTimestampFails`) and `ext` is the image file type. One counter example per failing assertion is enough. 

### Part III
- Put your answers into the given file `a3Part3.als` (see beginning of Part III). Please ensure that it is clear which (sub-question each answer corresponds to. 

**What and how to submit**

As for Assignments 1, submit your assignment before the deadline to **both** GitHub Classroom **and** OnQ. For the OnQ submission, download an archive of your repository **from GitHub** and upload it **as is** to OnQ (see submission instructions for Assignment 1 for more details).

## Alloy's visualizer
Alloy's visualization can be customized. The readability of instances with lots of different objects can be improved by

- having only some of the objects displayed, or by
- having the objects and relations displayed in different colors. 

To customize the visualizer, click "Theme" in the instance window. 
