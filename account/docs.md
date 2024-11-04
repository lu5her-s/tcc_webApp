# Account app

## Overview

This is the account app. It is used to manage user accounts.
Manage profile for users and change password.

## Models

- Sector : class -> for Sector workplace, ex. ทภ.1,2,3,4
- Department : class -> for Department workplace, ex. มทบ.11,22,33
- Rank : class -> for Rank of users
- Position : class -> for Position of users, ex. ส.อ., ร.อ.
- Profile : class -> for user profile
- LineToken : class -> for Line notify token
- user_directory_path(instance, filename) : function -> user directory path for save profile picture
- create_user_profile(sender, instance, created, **kwargs) : function -> create user profile
- save_user_profile(sender, instance, **kwargs) : function -> save user profile

## Views

- HomeView : class -> Index page, show Home page dashboard.
- RegisterView : class -> Register page, for register new user.
- ProfileView : class -> Profile page, for user profile. Update/Edit profile.
- ChangePassword : class -> Change password page.
- MembersListView : class -> List of members.
- MembersDetailView : class -> Detail of members.
- ContactView : class -> Contact page.
- update_profile(request) : function -> update user profile.
- sector_list(request, pk) : function -> list of sector
- position_list(request, pk) : function -> list of position
- check_username(request) : function -> check username for register page
