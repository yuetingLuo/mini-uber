# yueche

## Time Schedule

Jan 19: Complete project setup, finish Models.

Jan 20-24: One page per day.

Jan 25-27: Local integration testing.

Jan 28: Docker debugging (aiming for full website functionality by Jan 28).

Jan 29-Feb 7: Further Improvement.

## Progress

- [X] Create a user account

- [X] Login with a valid user account

- [X] Handle login failure with an an invalid user account

- [X] Logout from a user session

- [X] User should be able to register as a driver by entering their personal & vehicle info

- [X] User should be able to view and edit their driver status as well as personal & vehicle info 

- [X] User should be able to submit a ride request by specifying the required and any combination of the optional info

- [X] User should be able to make a selection to view any non-complete ride they belong to

- [X] User should be able to make a selection to edit any open ride they belong to

- [X] A ride owner should be able to edit the requested attributes of a ride until that ride is confirmed

- [X] User should be able to view all ride details for any open ride they belong to

- [X] User should be able to view all ride details + driver and vehicle details for any confirmed ride they belong to

- [X] User should be able to search for sharable, open ride requests (by destination, arrival window, and # of passengers)

- [X] User should be able to join a ride returned in a search as described in requirement #13

- [X] A registered driver should be able to search for open ride requests (filtered by the driver's vehicle capacity and type / special info, if applicable)

- [X] A registered driver should be able to mark a selected ride (returned from a search as described in requirement #15) as confirmed (thus claiming and starting the ride)

- [X] An email should be sent to the owner and any sharers of a ride once it is confirmed by a driver

- [X] A driver should be able to see a list of their confirmed rides

- [X] A driver should be able to select a confirmed ride and view all of the ride details

- [X] A driver should be able to edit a confirmed ride for the purpose of marking it complete after the ride is over

  
## Models

### 1. User
Derived fromdjango.contrib.auth.models.AbstractUser
id:primary key
username:string (e-mail)
password:string
vehicle:Vehicle

### 2. Ride
id:primary key
dest_addr:string
arrival_time:date&time
passenger_num:jsonb (user id corresponds to each person's passenger number) 
vehicle_type:string
sp_info:free text field
owner_id:int
driver_id:int
is_shared:bool
is_confirmed:bool
is_complete:bool

### 3. Vehicle
id:primary key
owner_id:foreignt_key
vehicle_type:string
license_id:int
capacity:int (maximum number of passengers)
sp_info:free text field


## Views（Categorized by URL path）

### Root Path /yueche
### Account（accountviews.py）

#### 1. /login

Name: login (used for URL reverse resolution, view function name also uses this)

Entry page of the website, where users input username (consider using email as username due to the need for sending emails) and password to log in, or click Create an account to register. Note, login and registration use methods from django.contrib.auth, and subsequent functional views should add the @login_required decorator to restrict access to authenticated users.

Sub-URL: 

1. /submit（login_submit）to submit login request.

#### 2. /

Name：root

Description：Redirects to /login

#### 3. /user-register

Name: user_register
Description: Account registration interface.
Related URL:
1. /submit (user_register_submit) to submit registration request.

#### 4. /main

Name: main
Description: User's main interface, with 5 buttons for different functionalities: "Launch ride", "Search for carpool", "Become driver/driver orders", "My rides", "Logout".
Related URL:
1. /logout (logout) to submit logout request.

#### 5. /driver-register

Name: driver_register
Description: Submit vehicle information to become a driver.
Related URL:
1. /submit (driver_register_submit) to submit registration request.

#### 6. /profile

Name: profile
Description: Personal information page, where users can modify their information.
Related URL:
1. /modify (profile_modify) to submit personal information modification request.

### Functionality （funcviews.py）

#### 7. /ride-launch

Name: ride_launch
Description: Ride owner launches a ride.
Related URL:
1. /submit (ride_launch_submit) to submit ride request.

#### 8. /ride-search/sharer

Name: ride_search_sharer
Description: Page for sharers to search and join orders.

#### 9. /ride-search/driver

Name: ride_search_driver
Description: Page for drivers to search and confirm orders.

#### 10. /ride-list/user 

Name: ride_list_user
Description: Displays all rides as a passenger.

#### 11. /ride-list/driver 

Name: ride_list_driver
Description: Displays all confirmed rides as a driver.

#### 12. /ride/<int:ride_id>

Name: ride_detail
Description: Ride detail page.
Related URL:
1. /quit (ride_quit) to cancel the ride.
2. /update (update_ride) to modify the ride (owner only).
3. /join (join_ride) to join the ride (only for sharers not yet joined).
4. /confirm (confirm_ride) to confirm the ride (drivers only).
5. /complete (complete_ride) to mark the ride as completed (drivers only).
