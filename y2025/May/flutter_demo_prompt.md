# How to create a demo from scratch with Cursor editor

## Initial command

Please write a flutter app, including following requirments:

1. The framework it depends on: Flutter@3.27.3, get@4.7.2
2. Also install framework if needed, use "fvm" for version management is preffered if needed.
3. The app is a news app, allow user to loggin with mobile phone numerber.
4. The app has 3 bottom tabs, the last is called "Mine".
5. The other 2 tabs is news list: "Recommend", "Subscription".
6. News list page has a top bar, and user can customize it by add or remove channels, or change the order, each channel could has sub tab bar for different content.
7. Using a public demo data source or dummy image to make it running.


## Following adjustment.

- I'd like to use fvm to manager version.
- It does not launch.
- It only shows a demo page, not the news app that I'd like to make.
- The version of Flutter should be locked on "3.27.3".
- What is version of Flutter we currently using? How do I change that?
- The channel edit button is not working as expected.
- The channel edit is not clickable, do you miss something?
- Well, iPhone 15 is good to go.
- Error: unable to find directory entry in pubspec.yaml: /Users/mayueyao/express_flutter_test/assets/images/
- The simulator did not running.
- Error: unable to find directory entry in pubspec.yaml: /Users/mayueyao/express_flutter_test/assets/images/
- When edit channel, it can not be removed from the list.
- We are under agent mode, try to resolve the issue: When edit channel, it can not be removed from the list.
- The channel can be removed now.
- But the result not reflected in the news list page.
- Oh no, it not working, the list not get updated.
- Can you show a debug version label on the scrren to let me confirm that it is on the right node, and increase the version number whenever you make the change and always tell me the version number.

## Some useful tips.

- Create a new session before a feature level task.
- Set rules for project level.
  - Always response in English.
  - Follow exits pattern already used in project.
  - When creat new feature, always try to used existing component and services.