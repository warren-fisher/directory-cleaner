# Directory-clean-by-age

 A python script to delete files and or folders over a certain age within a directory

## Features

- Can delete only files and/or only sub-directories
- Whitelist / blacklist files by extension type
- Recursively search sub-directories
- Delete files over a certain age
- Can be set to run periodically using task manager
- Windows support

## Getting Started

Getting started is easy. Python 3.6 is the lowest supported version because of F-strings.
The only dependency is Click, which is used for the command-line interface.

### Installing

#### Windows

1. Clone the github repo to a folder using

- `git clone https://github.com/warren-fisher/directory-cleaner.git folder_name`

2. Create a windows batch file somewhere on your computer that references the clean-by-age.py script

- `python C:path\clean-by-age.py`
- You can put this batch file somewhere on your computer and run it on-demand if desired.

3. To run it automatically use Windows Task Scheduler

- On windows 10 you can easily search by pressing [Windows Key] + [S]

4. Create a task

- Set name and description
- Navigating to triggers you can add a new trigger as desired.
- To run it periodically:
    - Select 'On a schedule' for desired method to start
    - Set it as one time
    - Select 'repeat task every:' and select a desired frequency and duration of this script
    - (Optional) Select 'stop task if it runs longer than' and select a time if you would like it to not run in the background for longer than a specified time.
    - Make sure enabled is selected
- Navigate to actions and add a new action
- Select 'Start a program' and
- Select the location of the program or script
- Other settings are as desired

5. Navigate to the clean-by-age.py in the installed directory
- Edit the python script and change the first five variables to your desired settings
Your script should now be set to run automatically. You can also run the python script 'clean-by-age.py' or the .bat file you created to run the script manually.

#### Linux 

Theoretically Linux should be supported. Initial testing was done and the test suite passed, although it is far from complete.
I would use at your own risk. 

## Planned features

- [x] indicates that a feature is in progress

- [x] Whitelist / blacklist by file type
- [x] Recursive deletions
- [x] Use OOP to allow for multiple folders to be tracked with different specifications
- [x] CLI for adding folders, changing specifications
- [ ] Linux support

    - [ ] Upgrade test suite
- [ ] Create built in schduler using sched
- [ ] Allow for using functions to determine how old files can be given the percent full your disk is
- [ ] Type annotations
