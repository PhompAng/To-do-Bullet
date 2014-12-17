To-Do Bullet
============
> *"Add once, notify on all devices."*

A to-do list application with push notification (via PushBullet).

**An internet connection is require while running this application.**

## Installation
1. Install PIL, using a precompiled binary *(http://www.pythonware.com/products/pil/)*.
2. Install MySQLdb (MySQL-python) *(http://www.codegood.com/archives/129/)*.
3. Run the main.py to launch the application.

## Using Instruction
First of all, you'll need to setup your PushBullet account and install its client (cross-platform available) on the device which you want To-Do Bullet to send a notification to. Then obtain your "Access Token" to use with this app. An instruction is listed below.

1. Sign up for PushBullet account [PushBullet website](https://www.pushbullet.com/).
2. Install the PushBullet client (Android, iOS, or even Chrome extension!) on the device you want to get notify on.
3. Get your "Access Token" from your [PushBullet account page](https://www.pushbullet.com/account).
4. Launch To-Do Bullet.
5. Insert your access token by go to File > Setting.
6. Try adding a task with date and time set to the future (If no time is set or it set to the past, no notification will be sent).

##### Adding a single task
1. Click on "Task" button.
2. Type your desired title and message.
3. Click "Add Task" button.

##### Adding a task list
1. Click on "List" button.
2. Type you list in the message field with the following format (`Item 1, Item 2, Item 2, ..., Item n`).
3. Click "Add Task" button.

##### Adding a task with link
1. Click on "List" button.
2. Type you desired title and put the URL of the destination website in the message field.
3. Click "Add Task" button.

##### Adding a task with file
1. Click on "List" button.
2. Type you desired title and put the URL of the file in the message field.
3. Click "Add Task" button.
