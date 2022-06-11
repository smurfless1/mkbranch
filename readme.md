# mkbranch for Jira compliant branches

# Install

This installs it in your existing go directory, if you have one.

`go install github.com/smurfless1/mkbranch@latest`

# Explain

A relatively simple task - make my branches for me.

Work asks me to use the following form:

`$USER/$ticket/$description`

which usually turns into things like:

```text
smurfless1/NO-JIRA/2022-05-10-fixin-stuff
smurfless1/PLATFORM-12345/2010-01-03-never-did-finish-this
smurfless1/PLATFORM-12345/2008-03-26-what-was-i-thinking
```

but I tend to squash my merges when it's time to have them
reviewed, and those I like to remove the date from, like this:

```text
smurfless1/NO-JIRA/fixin-stuff
smurfless1/PLATFORM-12345/never-did-finish-this
smurfless1/PLATFORM-12345/what-was-i-thinking
```

And so this little lame utility was born. 

# Show

My flow then becomes similar to this:

```shell

git checkout main
mkbranch fixin-stuff
# now on smurfless1/NO-JIRA/2022-05-10-fixin-stuff
git commit -m incomplete
git commit -m late
git checkout main
mkbranch --jira PLATFORM-12345 bugfix/get-around-to-it
# now on smurfless1/PLATFORM-12345/2022-05-10-bugfix/get-around-to-it
git commit -m vacation
# decide to open the pull request
# install your tab completion for best results
git switch smurfless1/NO-JIRA/2022-05-10-fixin-stuff
mkbranch --no-date fixin-stuff
# now on smurfless1/NO-JIRA/fixin-stuff
git push -u origin HEAD
```

## Go off topic

I love knowing when I created my various branches. It gives me a timeline for the
detritus in my branch list, and I can tell which ones are meant for PR because those are the ones without dates. 

* Could I have done this in another language? Yes, and I did, but interpreted languages keep breaking my environments, 
and this just plain runs faster. 
* Could I have done some magic inside the gitconfig? Maybe, but what's the fun in that?

