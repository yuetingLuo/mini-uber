1. **Passenger Join Restrictions**
   - Description: Passengers should not be able to join a ride they have already joined or created themselves.
   - Proposed Solution: Implement checks to prevent users from joining rides they are associated with as creators or previous joiners.
2. **Self-Driving Prevention**
   - Description: Passengers cannot act as their own driver in the ride-sharing application.
   - Proposed Solution: Enforce validation to prevent users from assigning themselves as drivers for their rides.
3. **Ride Modification by Sharer**
   - Description: Sharers should be able to edit the rides they have joined, specifically to modify the number of participants.
   - Proposed Solution: Allow editing capabilities for sharers to adjust participation details in a ride.
4. **Email Dispatch Issues**
   - Description: Emails cannot be sent out from the Duke VM. 
   - Proposed Solution: Implement asynchronous execution with failure handling, including up to 3 retries for sending emails. Adopt Google API in the local environment
5. **Non-sharable Rides Searchability**
   - Description: An issue where unsharable rides can be found and accessed by sharers.
   - Proposed Solution: Adjust search filters to exclude unsharable rides from sharer search results.
6. **Database Concurrency Problem**
   - Description: Database operation may cause dirty read or dirty write.
   - Proposed Solution: Address concurrency issues by changing the database isolation level to serializable.
7. **Error Handling for Database Operations**
   - Description: Lack of proper error handling when database operations fail.
   - Proposed Solution: Develop and implement comprehensive error handling mechanisms for all database interactions.
8. **Unauthorized Access via URL**
   - Description: Unauthorized access to ride details, accepting rides, and registration pages through direct URL manipulation.
   - Proposed Solution: Implement robust access control checks to validate user permissions before displaying sensitive content or allowing certain actions.
9. **Database Confirmation Before Actions**
   - Description:  The ride detail information shown in the ride list might be outdated, causing some operations to be executed illegally.
   - Proposed Solution: Confirm again with database for qualifications before allowing confirmations for a ride by drivers or operations like quit, join, modify by passengers
10. **Empty Ride Listings**
    - Description: When no rides are available in the ride list, a blank page may cause confusion for the user.
    - Proposed Solution: Implement a user-friendly message or indicator when no rides are available for display.
11. **Server Script Execution Permissions in Docker**
    - Description: The script for running the server in Docker needs to be configured with executable permissions.
    - Proposed Solution: Adjust the Docker configuration to ensure the server startup script has the appropriate executable permissions.