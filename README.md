# CS111-Green-Utilities

Tools for **CS111 Green** course instructors.

## Installation

```bash
pip install --upgrade git+https://github.com/karolisr/CS111-Green-Utilities
```

In case this fails (on account of permissions) you may instead try:

```bash
sudo -H pip install --upgrade git+https://github.com/karolisr/CS111-Green-Utilities
```

or, if you do not like using sudo for various reasons, try:

```bash
pip install --user --upgrade git+https://github.com/karolisr/CS111-Green-Utilities
```

Details: These options are a way of getting around `pip` defaults to installing Python packages to a system directory (such as /usr/local/lib/python3.4). This often requires root access.

`pip --user` option  makes pip install packages in your home directory instead, which generally does not require special privileges.


## Download Materials

The simplest way to view the contents is to just download everything by clicking on the green `Clone or download` button. No git necessary. Email us any suggested changes.


## A Crash Course in Git Editing

This is not meant to replace reading, but it's a good refresher. Before you start editing, you should _always_ do a fresh `git pull` to make sure you have the latest version! 

Next, you can see the logs by using the option `log`:

`git log`

The current accounting of untracked and changed files between your local repository and can be seen with option `status`:

`git status`

After you make changes, you can `commit -a` (all of) them. This will bring up a text editor to allow you to provide useful commentary. Please do.

`git commit -a`

An empty message (no text commentary) will abort the commit process.

Then, the best course is to first `pull` to make sure that any changes in the meantime are merged and finally `push` to the remote repo.

*Other useful commands*

`git add [myfile]` adds new files to be tracked and committed.
`git checkout [myfile]` allows you to get a new version of an individual file, branch, and commit (specific archived version). It is relatively hard to reset changes, so be careful.

Finally, should you get a dreaded `CONFLICT` and you are still at the level of this cheatsheet, just stop and call me! That means that I edited something and you edited that same thing. Ideally, you would review the differences, edit all of the conflict marks, select the changes to be kept, and then formally resolve the conflict and submit/push the new version.